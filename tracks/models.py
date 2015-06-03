from django.db import models
from django.db.models import Count
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
import requests


class Track(TimeStampedModel):
    service_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    now_playing = models.BooleanField(default=False)
    establishment = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = _("Track")
        unique_together = (("service_id", "establishment"),)

    def __unicode__(self):
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
    def fetch_and_save_track(cls, service_id, establishment):
        response = requests.get(
            'http://api.deezer.com/track/{0}'.format(service_id))

        if response.status_code == 200:
            response_json = response.json()
            if 'error' not in response_json:
                track, __ = Track.objects.update_or_create(
                    defaults={'title': response_json['title'],
                              'artist': response_json['artist']['name']},
                    service_id=service_id,
                    establishment=establishment)
                return track
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
