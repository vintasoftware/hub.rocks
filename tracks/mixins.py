import time
import logging
import pylast
from collections import namedtuple
from random import randint

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model

import django_fanout

from tracks.serializers import TrackSerializer, TrackListSerializer
from tracks.models import Track

User = get_user_model()


class LastFMScrobblerMixin(object):

    def scrobble(self, artist, title, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        if settings.LASTFM_API_KEY and self.establishment.lastfm_username:
            network = pylast.LastFMNetwork(
                api_key=settings.LASTFM_API_KEY,
                api_secret=settings.LASTFM_API_SECRET,
                username=self.establishment.lastfm_username,
                password_hash=self.establishment.lastfm_hashed_password)

            network.scrobble(artist=artist, title=title, timestamp=timestamp)
        else:
            logging.info("last.fm not setup, would scrobble {} for {}".format(
                         title, self.establishment.username))


class EstablishmentViewMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.establishment = get_object_or_404(
            User, username=kwargs['establishment'])
        return super(EstablishmentViewMixin, self).dispatch(request,
                                                            *args,
                                                            **kwargs)


class GetTokenMixin(object):

    def get_token(self):
        auth_header = self.request.META.get('HTTP_AUTHORIZATION', '')
        splitted_auth_header = auth_header.split(' ')

        if any(splitted_auth_header):
            __, token = splitted_auth_header
        else:
            token = None
        return token


class SerializeTrackListMixin(EstablishmentViewMixin):

    def get_now_playing(self):
        try:
            return Track.objects.get(now_playing=True,
                                     establishment=self.establishment)
        except Track.DoesNotExist:
            return None

    def track_list_serialize(self):
        qs = Track.ordered_qs(establishment=self.establishment)
        PlayList = namedtuple('PlayList', ['tracks', 'now_playing'])
        return TrackListSerializer(PlayList(qs, self.get_now_playing()))


class BroadCastTrackChangeMixin(LastFMScrobblerMixin, SerializeTrackListMixin):

    def publish(self, channel, data):
        channel = '{}-{}'.format(channel, self.establishment)
        if settings.FANOUT_REALM and settings.FANOUT_KEY:
            django_fanout.publish(channel, data)
        else:
            logging.info("Fanout not setup, would push {} to /{}".format(
                data, channel))

    def broadcast_list_changed(self):
        self.publish('tracks', self.track_list_serialize().data)

    def broadcast_track_changed(self, track):
        self.publish('player', TrackSerializer(track).data)
        if (track and track.service == Track.SERVICES.deezer and
                track.votes.count() > 0):
            try:
                self.scrobble(track.artist, track.title)
            except (pylast.WSError, IndexError):
                # there is a bug in current version that raises IndexError
                # at some cases
                pass
        self.broadcast_list_changed()


class SkipTrackMixin(BroadCastTrackChangeMixin):

    def stop_track(self, track):
        track.votes.all().delete()
        track.now_playing = False
        track.save()

    def safe_set_now_playing_track(self, track):
        try:
            with transaction.atomic():
                # make sure we don't have a race condition and end up with
                # two tracks now_playing
                track.now_playing = True
                track.played_on_random = True
                track.save()
                assert Track.objects.filter(now_playing=True,
                                            establishment=self.establishment
                                            ).count() == 1
        except AssertionError:
            pass

    def skip(self):
        try:
            current = Track.objects.get(now_playing=True,
                                        establishment=self.establishment)
            self.stop_track(current)
            qs = Track.objects.filter(now_playing=False,
                                      establishment=self.establishment
                                      ).exclude(id=current.id)
        except Track.DoesNotExist:
            current = None
            qs = Track.objects.filter(establishment=self.establishment,
                                      now_playing=False)

        # use current to prevent skip to the same song
        # get the first by vote
        if current is not None:
            track = Track.ordered_qs(establishment=self.establishment
                                     ).exclude(id=current.id).first()
        else:
            track = Track.ordered_qs(establishment=self.establishment
                                     ).first()

        # get random
        if not track:
            new_qs = qs.filter(played_on_random=False)
            if new_qs.exists():
                qs = new_qs
            else:
                qs.update(played_on_random=False)
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
            self.safe_set_now_playing_track(track)
            self.broadcast_track_changed(track)
            return track
