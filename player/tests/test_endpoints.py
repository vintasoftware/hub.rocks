
from django.core.urlresolvers import reverse

from rest_framework import status
from mock import patch

from tracks.mixins import BroadCastTrackChangeMixin
from tracks.tests.utils import TrackAPITestCase


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
