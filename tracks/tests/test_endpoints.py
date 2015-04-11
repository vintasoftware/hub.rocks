
from django.core.urlresolvers import reverse

from rest_framework import status
from model_mommy import mommy
from mock import patch

from tracks.models import Track
from tracks.endpoints import VoteAPIView, SkipTrackAPIView
from tracks.tests.utils import TrackTestCase


class VoteSkipNowPlayingAPIViewTestCase(TrackTestCase):

    def request(self, establishment):
        url = reverse('api:now-playing-skip',
                      kwargs={'establishment': establishment.username})
        return self.client.post(url, {'service_id': self.track.service_id})

    def test_skip_when_no_votes(self):
        response = self.request(self.establishment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.track = Track.objects.get(id=self.track.id)
        self.track_not_playing = Track.objects.get(
            id=self.track_not_playing.id)
        self.assertFalse(self.track.now_playing)
        self.assertTrue(self.track_not_playing.now_playing)

    def test_skip_with_votes(self):
        mommy.make('Vote', track=self.track)
        response = self.request(self.establishment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.track = Track.objects.get(id=self.track.id)
        self.assertTrue(self.track.now_playing)
        self.assertEqual(self.track.votes.first().skip_request_by, 'foo')

    def test_twice_skip_with_votes(self):
        mommy.make('Vote', track=self.track)
        response = self.request(self.establishment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.request(self.establishment)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.track = Track.objects.get(id=self.track.id)
        self.assertTrue(self.track.now_playing)
        self.assertEqual(self.track.votes.first().skip_request_by, 'foo')

    def test_skip_track_from_other_establishment(self):
        response = self.request(mommy.make('User'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TrackListAPIViewTestCase(TrackTestCase):

    def request(self, establishment):
        url = reverse('api:list',
                      kwargs={'establishment': establishment.username})
        return self.client.get(url)

    def test_get(self):
        response = self.request(self.establishment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['now_playing']['service_id'],
                         self.track.service_id)
        self.assertEqual(len(response.data['tracks']), 1)
        self.assertEqual(response.data['tracks'][0]['service_id'],
                         self.track_not_playing.service_id)


class VoteAPIViewTestCase(TrackTestCase):

    def get_url(self, establishment, service_id):
        return reverse('api:vote',
                       kwargs={'establishment': establishment.username,
                               'service_id': service_id})

    @staticmethod
    def create_track(service_id, establishment):
        Track.objects.update_or_create(
                             defaults={'title': 'foo', 'artist': 'bar'},
                             service_id=service_id,
                             establishment=establishment)

    @patch.object(VoteAPIView, 'broadcast_list_changed')
    def test_vote_existing_track(self, mock):
        with patch.object(Track, 'fetch_and_save_track',
                          side_effect=self.create_track):
            response = self.client.post(self.get_url(self.establishment,
                                                     self.track.service_id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.track.votes.count(), 1)
        self.assertEqual(mock.call_count, 1)

    @patch.object(VoteAPIView, 'broadcast_list_changed')
    def test_vote_new_track(self, mock):

        with patch.object(Track, 'fetch_and_save_track',
                          side_effect=self.create_track):
            response = self.client.post(self.get_url(self.establishment,
                                                     '22222'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        track = Track.objects.get(establishment=self.establishment,
                                  service_id='22222')
        self.assertEqual(track.votes.count(), 1)
        self.assertEqual(mock.call_count, 1)

    @patch.object(VoteAPIView, 'broadcast_list_changed')
    def test_unvote_existing_track(self, mock):
        with patch.object(Track, 'fetch_and_save_track',
                          side_effect=self.create_track):
            response = self.client.post(self.get_url(self.establishment,
                                                     self.track.service_id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.track.votes.count(), 1)
        response = self.client.delete(self.get_url(self.establishment,
                                                   self.track.service_id))
        self.assertEqual(self.track.votes.count(), 0)
        self.assertEqual(mock.call_count, 2)


class NowPlayingAPIView(TrackTestCase):

    def test_get(self):
        response = self.client.get(reverse('api:now-playing',
                                           kwargs={'establishment':
                                                   self.establishment}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['service_id'], self.track.service_id)


class SkipTrackAPIView(TrackTestCase):

    @patch.object(SkipTrackAPIView, 'broadcast_list_changed')
    def test_post(self, mock):
        response = self.client.post(reverse('api:next', kwargs={
                                            'establishment':
                                            self.establishment}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mock.call_count, 1)
