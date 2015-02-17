from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from request.exceptions import RequestException

from tracks.models import Track, Vote
from tracks.token import get_token


class VoteCreateAPIView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        if not Track.objects.filter(
            service_id=self.service_id).exists():
            try:
                Track.fetch_and_save_track()
            except RequestException:
                return Response(
                    status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except ValueError:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST)

        return super(VoteCreateAPIView,
            self).create(request, *args, **kwargs)


class VoteDeleteAPIView(generics.DeleteAPIView):
    
    def get_object(self, *args, **kwargs):
        return get_object_or_404(Vote,
            track=self.kwargs['service_id'],
            token=get_token())
