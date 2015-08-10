
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from mock import patch

from tracks.mixins import BroadCastTrackChangeMixin
from tracks.tests.utils import TrackAPITestCase
from player.models import PlayerStatus

User = get_user_model()


class SkipTrackAPIViewTestCase(TrackAPITestCase):

    def setUp(self):
        super(SkipTrackAPIViewTestCase, self).setUp()
        self.client.login(username='establishment', password='bar')

    @patch.object(BroadCastTrackChangeMixin, 'broadcast_list_changed')
    def test_post(self, mock):
        response = self.client.post(reverse('api-player:next'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mock.call_count, 1)

    def test_non_authed(self):
        self.client.logout()
        response = self.client.post(reverse('api-player:next'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NowPlayingAPIViewTestCase(TrackAPITestCase):

    def setUp(self):
        super(NowPlayingAPIViewTestCase, self).setUp()
        self.client.login(username='establishment', password='bar')

    def test_get(self):
        response = self.client.get(reverse('api-player:now-playing'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['service_id'], self.track.service_id)


class PlayingStatusAPIViewTestCase(TrackAPITestCase):

    def setUp(self):
        super(PlayingStatusAPIViewTestCase, self).setUp()
        self.client.login(username='establishment', password='bar')

    def test_put_new(self):
        self.assertEqual(PlayerStatus.objects.count(), 0)
        response = self.client.put(reverse('api-player:change-status'),
                                   {'playing': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PlayerStatus.objects.count(), 1)

    def test_put_existing(self):
        ps = PlayerStatus.objects.create(establishment=self.establishment)
        self.assertFalse(ps.playing)

        response = self.client.put(reverse('api-player:change-status'),
                                   {'playing': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PlayerStatus.objects.get(id=ps.id).playing)
        self.assertEqual(PlayerStatus.objects.count(), 1)

    def test_without_login(self):
        self.client.logout()
        response = self.client.put(reverse('api-player:change-status'),
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
        response = self.client.put(reverse('api-player:change-status'),
                                   {'establishment': self.establishment.id,
                                    'playing': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(PlayerStatus.objects.get(id=ps.id).playing)
