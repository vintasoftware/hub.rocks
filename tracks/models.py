from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
import requests


class Track(TimeStampedModel):
    service_id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    now_playing = models.BooleanField(default=False)
    on_queue = models.BooleanField(default=True)

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
            filter(now_playing=False, on_queue=True).
            annotate(votes_count=Count('votes')).
            order_by('-votes_count', 'modified'))

    @classmethod
    def fetch_and_save_track(cls, service_id):
        response = requests.get(
            'http://api.deezer.com/track/{0}'.format(service_id))
        
        if response.status_code == 200:
            response_json = response.json()
            if 'error' not in response_json:
                track, __ = Track.objects.update_or_create(
                    defaults={'on_queue': True,
                              'title': response_json['title'],
                              'artist': response_json['artist']['name']},
                    service_id=service_id)
                return track
            else:
                raise ValueError("Deezer error")
        else:
            raise ValueError("Deezer response != 200")


class Vote(TimeStampedModel):
    track = models.ForeignKey(Track, related_name='votes')
    token = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Vote")
        unique_together = ('track', 'token')
