from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from requests.exceptions import RequestException

from tracks.serializers import VoteSerializer
from tracks.models import Track, Vote


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

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Vote,
            track=self.kwargs['service_id'],
            token=self.get_token())

    def get_serializer(self, *args, **kwargs):
        kwargs['data'] = dict(kwargs['data'])
        data = kwargs['data']
        
        data['token'] = self.get_token()
        data['track'] = self.kwargs['service_id']
        
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

