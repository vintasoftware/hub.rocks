from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import generics, status
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from requests.exceptions import RequestException

from tracks.serializers import (
    TrackSerializer, VoteSerializer)
from tracks.models import Track, Vote, NowPlaying


class TracksAPIView(generics.ListAPIView):
    serializer_class = TrackSerializer

    def get_queryset(self):
        return (Track.objects.
            annotate(votes_count=Count('votes')).
            order_by('-votes_count', 'modified'))

    def get(self, request, *args, **kwargs):
        response = super(TracksAPIView,
            self).get(request, *args, **kwargs)
        
        response_data = response.data
        response.data = {}
        response.data['tracks'] = response_data
        try:
            response.data['now_playing'] = TrackSerializer(
                NowPlaying.objects.get().track).data
        except NowPlaying.DoesNotExist:
             response.data['now_playing'] = None

        return response


class VoteAPIView(DestroyModelMixin, generics.CreateAPIView):
    serializer_class = VoteSerializer

    def get_token(self):
        auth_header = self.request.META.get('HTTP_AUTHORIZATION', '')
        splitted_auth_header = auth_header.split(' ')
        
        if len(splitted_auth_header):
            __, token = splitted_auth_header
        else:
            token = None
        
        return token

    def get_serializer(self, *args, **kwargs):
        kwargs['data'] = {}
        kwargs['data']['token'] = self.get_token()
        kwargs['data']['track'] = self.kwargs['service_id']
        
        return super(VoteAPIView,
            self).get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        service_id = self.kwargs['service_id']

        if not Track.objects.filter(
            service_id=service_id).exists():
            try:
                Track.fetch_and_save_track(service_id)
            except RequestException:
                return Response(
                    status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except ValueError:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST)

        return super(VoteAPIView,
            self).create(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Vote,
            track=self.kwargs['service_id'],
            token=self.get_token())

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class NowPlayingAPIView(DestroyModelMixin, generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        service_id = self.kwargs['service_id']

        if not Track.objects.filter(
            service_id=service_id).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST)

        NowPlaying.objects.update(track=service_id)

        return Response(status=status.HTTP_200_OK)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(NowPlaying,
            track=self.kwargs['service_id'])

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
