from django.db import models
from django.db.models import Count
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from model_utils import Choices
import requests


class Track(TimeStampedModel):
    SERVICES = Choices(('deezer', 'Deezer'), ('youtube', 'YouTube'))
    service = models.CharField(choices=SERVICES, default=SERVICES.deezer,
                               max_length=20)
    service_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    now_playing = models.BooleanField(default=False)
    establishment = models.ForeignKey(settings.AUTH_USER_MODEL)
    played_on_random = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Track")
        unique_together = (("service_id", "establishment", "service"),)

    def __str__(self):
        return u"Track {}: {} - {}".format(
            self.service_id,
            self.artist,
            self.title)

    @classmethod
    def ordered_qs(cls, establishment):
        return (Track.objects.
                filter(now_playing=False, votes__isnull=False,
                       establishment=establishment).
                annotate(votes_count=Count('votes')).
                order_by('-votes_count', 'modified'))

    @classmethod
    def _get_or_create_track(cls, title, artist, service, service_id,
                             establishment):
        track, __ = Track.objects.update_or_create(defaults={'title': title,
                                                             'artist': artist},
                                                   service=service,
                                                   service_id=service_id,
                                                   establishment=establishment)
        return track

    @classmethod
    def fetch_and_save_track(cls, service, service_id, establishment):
        kwargs = {'service': service, 'service_id': service_id,
                  'establishment': establishment}
        if service == cls.SERVICES.deezer:
            response = requests.get(
                'http://api.deezer.com/track/{0}'.format(service_id))

            if response.status_code == 200:
                response_json = response.json()
                if 'error' not in response_json:
                    kwargs.update({'title': response_json['title'],
                                   'artist': response_json['artist']['name']})
                else:
                    raise ValueError("Deezer error")
            else:
                raise ValueError("Deezer response != 200")
        else:
            response = requests.get(
                'https://www.googleapis.com/youtube/v3/videos?part=snippet&'
                'id={}&key={}'.format(service_id, settings.YOUTUBE_KEY))
            if response.status_code == 200:
                response_json = response.json()
                if response_json['items']:
                    snippet = response_json['items'][0]['snippet']
                    kwargs.update({'title': snippet['title'],
                                   'artist': snippet['channelTitle'] or
                                   'unknown'})
                else:
                    raise ValueError("YouTube error")
            else:
                raise ValueError("YouTube response != 200")
        return cls._get_or_create_track(**kwargs)


class Vote(TimeStampedModel):
    track = models.ForeignKey(Track, related_name='votes')
    token = models.CharField(max_length=255)

    # This field is used to cancel a vote. Votes can be cancelled by anyone
    # that clicks on skip. When there is no vote left to be cancelled and
    # a skip request is made, the song will be skipped.
    # The result is that when votes + 1 skip requests are made the track
    # will be skipped.
    skip_request_by = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        verbose_name = _("Vote")
        unique_together = ('track', 'token')
