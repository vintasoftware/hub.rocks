
import copy

from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from tracks.mixins import SkipTrackMixin
from tracks.models import Track
from tracks.serializers import TrackSerializer

from player.mixins import PlayerEndpointMixin
from player.serializers import PlayerStatusSerializer
from player.models import PlayerStatus


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


class PlayingStatusAPIView(PlayerEndpointMixin,
                           generics.UpdateAPIView):
    serializer_class = PlayerStatusSerializer

    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data'):
            data = copy.copy(kwargs.get('data'))
            data['establishment'] = self.establishment.pk
            kwargs = copy.copy(kwargs)
            kwargs['data'] = data
        return super(PlayingStatusAPIView, self).get_serializer(*args,
                                                                **kwargs)

    def get_object(self):
        return PlayerStatus.objects.get_or_create(
            establishment=self.establishment)[0]
