
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from tracks.mixins import SkipTrackMixin
from tracks.models import Track
from tracks.serializers import TrackSerializer

from player.mixins import PlayerEndpointMixin


class SkipTrackAPIView(PlayerEndpointMixin, SkipTrackMixin,
                       generics.GenericAPIView):
    serializer_class = TrackSerializer

    def post(self, request, *args, **kwargs):
        track = self.skip()
        if track is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class NowPlayingAPIView(PlayerEndpointMixin,
                        generics.RetrieveAPIView):
    serializer_class = TrackSerializer

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Track, now_playing=True,
                                 establishment=self.establishment)
