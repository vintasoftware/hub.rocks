from collections import namedtuple
from random import randint

from django.db import transaction

import django_fanout

from tracks.serializers import TrackSerializer, TrackListSerializer
from tracks.models import Track


class GetTokenMixin(object):

    def get_token(self):
        auth_header = self.request.META.get('HTTP_AUTHORIZATION', '')
        splitted_auth_header = auth_header.split(' ')

        if len(splitted_auth_header):
            __, token = splitted_auth_header
        else:
            token = None
        return token


class SerializeTrackListMixin(object):

    def get_now_playing(self):
        try:
            return Track.objects.get(now_playing=True)
        except Track.DoesNotExist:
            return None

    def track_list_serialize(self):
        qs = Track.ordered_qs()
        PlayList = namedtuple('PlayList', ['tracks', 'now_playing'])
        return TrackListSerializer(PlayList(qs, self.get_now_playing()))


class BroadCastTrackChangeMixin(SerializeTrackListMixin):

    def broadcast_list_changed(self):
        django_fanout.publish('tracks', self.track_list_serialize().data)

    def broadcast_track_changed(self, track):
        django_fanout.publish('player', TrackSerializer(track).data)
        self.broadcast_list_changed()


class SkipTrackMixin(BroadCastTrackChangeMixin):

    def stop_track(self, track):
        track.votes.all().delete()
        track.now_playing = False
        track.save()

    def skip(self):
        try:
            current = Track.objects.get(now_playing=True)
            self.stop_track(current)
            qs = Track.objects.filter(now_playing=False).exclude(id=current.id)
        except Track.DoesNotExist:
            current = None
            qs = Track.objects.filter(now_playing=False)

        # use current to prevent skip to the same song
        # get the first by vote
        if current is not None:
            track = Track.ordered_qs().exclude(id=current.id).first()
        else:
            track = Track.ordered_qs().first()

        # get random
        if not track:
            # select a track at random
            last = qs.count() - 1
            if last >= 0:
                index = randint(0, last)
                try:
                    track = qs[index]
                except IndexError:
                    # on the very unlikely event of selecting an index that
                    # disappeared between the two queries we try selecting the
                    # first one.
                    track = qs.first()

        if track:
            with transaction.atomic():
                # make sure we don't have a race condition and end up with
                # two tracks now_playing
                track.now_playing = True
                track.save()
                assert Track.objects.filter(now_playing=True).count() == 1
            self.broadcast_track_changed(track)
