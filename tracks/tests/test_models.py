
import json

from django.db import IntegrityError, transaction

import responses
from model_mommy import mommy

from tracks.models import Track
from tracks.tests.utils import TrackTestCase


class TrackTestCase(TrackTestCase):

    @staticmethod
    def request_callback_deezer(request):
        resp_body = {'artist': {'name': 'foo'},
                     'title': 'bar'}
        return (200, {}, json.dumps(resp_body))

    @staticmethod
    def request_callback_youtube(request):
        resp_body = {'items': [{'snippet': {'title': 'bar',
                                            'channelTitle': 'foo'}}]}
        return (200, {}, json.dumps(resp_body))

    @responses.activate
    def test_fetch_and_save_when_new_deezer(self):
        x = Track.objects.all().count()
        responses.add_callback(
            responses.GET, 'http://api.deezer.com/track/223456',
            callback=self.request_callback_deezer,
            content_type='application/json',
        )
        track = Track.fetch_and_save_track(Track.SERVICES.deezer, '223456',
                                           self.establishment)
        self.assertTrue(Track.objects.filter(id=track.id).exists())
        self.assertEqual(Track.objects.all().count(), x + 1)

    @responses.activate
    def test_fetch_and_save_when_existing_deezer(self):
        x = Track.objects.all().count()
        responses.add_callback(
            responses.GET, ('http://api.deezer.com/track/%s' %
                            self.track.service_id),
            callback=self.request_callback_deezer,
            content_type='application/json',
        )
        Track.fetch_and_save_track(Track.SERVICES.deezer,
                                   self.track.service_id, self.establishment)
        self.assertEqual(Track.objects.all().count(), x)

    @responses.activate
    def test_fetch_and_save_when_new_youtube(self):
        x = Track.objects.all().count()
        responses.add_callback(
            responses.GET, 'https://www.googleapis.com/youtube/v3/videos',
            callback=self.request_callback_youtube,
            content_type='application/json',
        )
        track = Track.fetch_and_save_track(Track.SERVICES.youtube, '223456',
                                           self.establishment)
        self.assertTrue(Track.objects.filter(id=track.id).exists())
        self.assertEqual(Track.objects.all().count(), x + 1)

    @responses.activate
    def test_fetch_and_save_when_existing_youtube(self):
        x = Track.objects.all().count()
        responses.add_callback(
            responses.GET, 'https://www.googleapis.com/youtube/v3/videos',
            callback=self.request_callback_youtube,
            content_type='application/json',
        )
        Track.fetch_and_save_track(Track.SERVICES.youtube,
                                   self.track_youtube.service_id,
                                   self.establishment)
        self.assertEqual(Track.objects.all().count(), x)

    def test_unique_together(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Track.objects.create(service_id=self.track.service_id,
                                     establishment=self.establishment)
        establishment = mommy.make('Account')
        Track.objects.create(service_id=self.track.service_id,
                             establishment=establishment)
