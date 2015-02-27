from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from requests.exceptions import RequestException

from tracks.serializers import (
    TrackSerializer, VoteSerializer,
    TrackUpdateSerializer)
from tracks.models import Track, Vote
from core.mixins import PusherMixin


class TrackListAPIView(generics.ListAPIView):
    serializer_class = TrackSerializer

    def get_queryset(self):
        return Track.ordered_qs()

    def get(self, request, *args, **kwargs):
        response = super(TrackListAPIView,
            self).get(request, *args, **kwargs)
        
        response_data = response.data
        response.data = {}
        response.data['tracks'] = response_data
        try:
            response.data['now_playing'] = TrackSerializer(
                Track.objects.get(now_playing=True)).data
        except Track.DoesNotExist:
             response.data['now_playing'] = None

        return response


class VoteAPIView(PusherMixin, mixins.DestroyModelMixin, generics.CreateAPIView):
    serializer_class = VoteSerializer
    pusher_channel = 'tracks'
    pusher_event = 'updated'

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

    def perform_destroy(self, instance):
        super(VoteAPIView, self).perform_destroy(instance)

        if Vote.objects.filter(
            track=instance.track).count() == 0:
            # if track has no other votes, delete it
            instance.track.delete()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class NowPlayingAPIView(PusherMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrackUpdateSerializer
    pusher_channel = 'tracks'
    pusher_event = 'updated'

    def get_object(self, *args, **kwargs):
        if self.request.method == 'PUT':
            if 'service_id' in self.request.DATA:
                return get_object_or_404(Track,
                    service_id=self.request.DATA['service_id'])
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return get_object_or_404(Track, now_playing=True)


class NextTrackAPIView(generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        qs = Track.ordered_qs()    
        
        if qs.exists():
            data = TrackSerializer(qs[0]).data
        else:
            data = None

        return Response({'next': data})
