
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from model_mommy import mommy
from mock import patch

from tracks.models import Track
from tracks.endpoints import VoteAPIView, InsertTrackAPIView
from tracks.tests.utils import TrackAPITestCase
from player.models import PlayerStatus

User = get_user_model()


class VoteSkipNowPlayingAPIViewTestCase(TrackAPITestCase):

    def request(self, establishment):
        url = reverse('api:now-playing-skip',
                      kwargs={'establishment': establishment.username})
        return self.client.post(url, {'track_id': self.track.id})

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
        response = self.request(mommy.make('Account'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TrackListAPIViewTestCase(TrackAPITestCase):

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


class InsertTrackAndVoteAPIViewTestCase(TrackAPITestCase):

    def get_insert_url(self, service_id, service):
        return reverse('api:insert',
                       kwargs={'establishment': self.establishment.username,
                               'service_id': service_id, 'service': service})

    def get_vote_url(self, track_id):
        return reverse('api:vote',
                       kwargs={'establishment': self.establishment.username,
                               'track_id': track_id})

    @staticmethod
    def create_track(service, service_id, establishment):
        return Track.objects.update_or_create(
            service=service,
            defaults={'title': 'foo', 'artist': 'bar'},
            service_id=service_id,
            establishment=establishment)[0]

    @patch.object(InsertTrackAPIView, 'broadcast_list_changed')
    def test_vote_existing_track(self, mock):
        with patch.object(Track, 'fetch_and_save_track',
                          side_effect=self.create_track):
            response = self.client.post(self.get_insert_url(
                                                     self.track.service_id,
                                                     'deezer'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.track.votes.count(), 1)
        self.assertEqual(mock.call_count, 1)

    @patch.object(InsertTrackAPIView, 'broadcast_list_changed')
    def test_vote_new_track(self, mock):

        with patch.object(Track, 'fetch_and_save_track',
                          side_effect=self.create_track):
            response = self.client.post(self.get_insert_url('22222', 'deezer'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        track = Track.objects.get(establishment=self.establishment,
                                  service_id='22222')
        self.assertEqual(track.votes.count(), 1)
        self.assertEqual(mock.call_count, 1)

    @patch.object(VoteAPIView, 'broadcast_list_changed')
    @patch.object(InsertTrackAPIView, 'broadcast_list_changed')
    def test_unvote_existing_track(self, mock1, mock2):
        with patch.object(Track, 'fetch_and_save_track',
                          side_effect=self.create_track):
            url = self.get_insert_url(self.track.service_id, 'deezer')
            response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.track.votes.count(), 1)
        response = self.client.delete(self.get_vote_url(self.track.id))
        self.assertEqual(self.track.votes.count(), 0)
        self.assertEqual(mock1.call_count, 1)
        self.assertEqual(mock2.call_count, 1)


class PlayingStatusAPIViewTestCase(TrackAPITestCase):

    def setUp(self):
        super(PlayingStatusAPIViewTestCase, self).setUp()
        self.client.login(username='establishment', password='bar')
        self.url = reverse('api:change-status',
                           kwargs={'establishment': self.establishment.username})

    def test_put_new(self):
        self.assertEqual(PlayerStatus.objects.count(), 0)
        response = self.client.put(self.url, {'playing': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PlayerStatus.objects.count(), 1)

    def test_put_existing(self):
        ps = PlayerStatus.objects.create(establishment=self.establishment)
        self.assertFalse(ps.playing)

        response = self.client.put(self.url, {'playing': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PlayerStatus.objects.get(id=ps.id).playing)
        self.assertEqual(PlayerStatus.objects.count(), 1)

    def test_without_login(self):
        self.client.logout()
        response = self.client.put(self.url,
                                   {'establishment': self.establishment.id,
                                    'playing': False})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(PlayerStatus.objects.count(), 0)

    def test_another_establishment(self):
        ps = PlayerStatus.objects.create(establishment=self.establishment)
        self.assertFalse(ps.playing)
        User.objects.create_user(username='foo', email='email@gmail.com',
                                 password='bar')
        self.client.login(username='foo', password='bar')
        response = self.client.put(self.url,
                                   {'establishment': self.establishment.id,
                                    'playing': True})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertFalse(PlayerStatus.objects.get(id=ps.id).playing)
