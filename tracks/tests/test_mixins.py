
from tracks.tests.utils import TrackTestCase
from tracks.mixins import SkipTrackMixin
from tracks.models import Track


class TestSkipTrackMixin(TrackTestCase):

    def test_cannot_set_two_as_now_playing(self):
        self.track.now_playing = False
        self.track.save()
        mixin = SkipTrackMixin()
        mixin.establishment = self.establishment
        mixin.safe_set_now_playing_track(self.track)
        mixin.safe_set_now_playing_track(self.track_not_playing)
        self.assertEqual(Track.objects.filter(now_playing=True).count(), 1)
