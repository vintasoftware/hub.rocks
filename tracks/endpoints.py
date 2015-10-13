from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, status, views, renderers
from rest_framework.response import Response
from requests.exceptions import RequestException

from player.serializers import PlayerStatusSerializer
from tracks.serializers import (
    VoteSerializer, TrackListSerializer, TrackSerializer)
from player.mixins import PlayingStatusMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from tracks.models import Track, Vote
from tracks.mixins import (
    GetTokenMixin, SkipTrackMixin, SerializeTrackListMixin,
    BroadCastTrackChangeMixin, EstablishmentViewMixin)


class VoteSkipNowPlayingAPIView(SkipTrackMixin, GetTokenMixin,
                                views.APIView):

    def post(self, request, *args, **kwargs):
        token = self.get_token()
        track_id = request.data.get('track_id')
        track = get_object_or_404(Track, id=track_id,
                                  establishment=self.establishment,
                                  now_playing=True)

        if token and not track.votes.filter(skip_request_by=token).exists():
            vote = Vote.objects.filter(track=track, skip_request_by='').first()
            if vote:
                vote.skip_request_by = token
                vote.save()
                self.broadcast_list_changed()
            else:
                # no vote left to cancel, that must be a bad song, skip it!
                self.skip()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ListCreateTrackAPIView(GetTokenMixin, BroadCastTrackChangeMixin,
                             generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TrackListSerializer
        else:
            return TrackSerializer

    def perform_create(self, serializer):
        try:
            super(ListCreateTrackAPIView, self).perform_create(serializer)
            Vote.objects.create(track=serializer.instance,
                                token=self.get_token())
        except RequestException:
            return Response(
                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ValueError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=e.message)
        self.broadcast_list_changed()

    def list(self, request, *args, **kwargs):
        serializer = self.track_list_serialize()
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(ListCreateTrackAPIView, self).get_serializer_context()
        context['establishment'] = self.establishment
        return context


class VoteAPIView(BroadCastTrackChangeMixin,
                  GetTokenMixin, mixins.DestroyModelMixin,
                  generics.CreateAPIView):
    serializer_class = VoteSerializer
    renderer_classes = [renderers.JSONRenderer]

    def get_serializer(self, *args, **kwargs):
        kwargs['data'] = {'token': self.get_token(),
                          'track': self.track.pk}
        return super(VoteAPIView, self).get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        track_id = self.kwargs['track_id']
        self.track = get_object_or_404(Track, id=track_id)
        return super(VoteAPIView, self).create(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(
            Vote,
            track__id=self.kwargs['track_id'],
            token=self.get_token())

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        response = super(VoteAPIView, self).dispatch(request, *args,
                                                     **kwargs)
        if 200 <= response.status_code < 300:
            self.broadcast_list_changed()
        return response


class PlayingStatusAPIView(EstablishmentViewMixin,
                           PlayingStatusMixin,
                           generics.RetrieveUpdateAPIView):
    serializer_class = PlayerStatusSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        if self.establishment == request.user:
            return super(PlayingStatusAPIView, self).put(request, *args, **kwargs)
        return self.http_method_not_allowed(request, *args, **kwargs)
