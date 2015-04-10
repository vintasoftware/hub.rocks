# encoding: utf-8

from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
import requests


class Track(TimeStampedModel):
    service_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    now_playing = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Track")

    def __unicode__(self):
        return u"Track {}: {} - {}".format(
            self.service_id,
            self.artist,
            self.title)

    @classmethod
    def ordered_qs(cls):
        return (Track.objects.
            filter(now_playing=False, votes__isnull=False).
            annotate(votes_count=Count('votes')).
            order_by('-votes_count', 'modified'))

    @classmethod
    def fetch_and_save_track(cls, service_id):
        response = requests.get(
            'http://api.deezer.com/track/{0}'.format(service_id))
        
        if response.status_code == 200:
            response_json = response.json()
            if (response_json['artist']['id'] == 7691 and
                    response_json['title'].lower() != u'anna júlia'):
                raise ValueError("Los Hermanos Error")
            if 'error' not in response_json:
                return Track.objects.create(
                    title=response_json['title'],
                    artist=response_json['artist']['name'],
                    service_id=service_id)
            else:
                raise ValueError("Deezer error")
        else:
            raise ValueError("Deezer response != 200")


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
