
import json

from django.db import IntegrityError, transaction

import responses
from model_mommy import mommy

from tracks.models import Track
from tracks.tests.utils import TrackTestCase


class TrackTestCase(TrackTestCase):

    @staticmethod
    def request_callback(request):
        resp_body = {'artist': {'name': 'foo'},
                     'title': 'bar'}
        return (200, {}, json.dumps(resp_body))

    @responses.activate
    def test_fetch_and_save_when_new(self):
        x = Track.objects.all().count()
        responses.add_callback(
            responses.GET, 'http://api.deezer.com/track/223456',
            callback=self.request_callback,
            content_type='application/json',
        )
        track = Track.fetch_and_save_track('223456', self.establishment)
        self.assertTrue(Track.objects.filter(id=track.id).exists())
        self.assertEqual(Track.objects.all().count(), x + 1)

    @responses.activate
    def test_fetch_and_save_when_existing(self):
        x = Track.objects.all().count()
        responses.add_callback(
            responses.GET, ('http://api.deezer.com/track/%s' %
                            self.track.service_id),
            callback=self.request_callback,
            content_type='application/json',
        )
        Track.fetch_and_save_track(self.track.service_id, self.establishment)
        self.assertEqual(Track.objects.all().count(), x)

    def test_unique_together(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Track.objects.create(service_id=self.track.service_id,
                                     establishment=self.establishment)
        establishment = mommy.make('Account')
        Track.objects.create(service_id=self.track.service_id,
                             establishment=establishment)
