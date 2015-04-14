

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from tracks.mixins import SkipTrackMixin, EstablishmentViewMixin
from tracks.serializers import TrackSerializer


class SkipTrackAPIView(SkipTrackMixin, generics.GenericAPIView):
    serializer_class = TrackSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        self.establishment = request.user
        return super(EstablishmentViewMixin, self).dispatch(request,
                                                            *args,
                                                            **kwargs)

    def post(self, request, *args, **kwargs):
        self.skip()
        return Response(status=status.HTTP_200_OK)
