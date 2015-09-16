import copy

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from player.models import PlayerStatus
from tracks.mixins import EstablishmentViewMixin


class PlayerEndpointMixin(object):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        self.establishment = request.user
        # This replaces behaviour of EstablishmentViewMixin
        if isinstance(self, EstablishmentViewMixin):
            return super(EstablishmentViewMixin, self).dispatch(request,
                                                                *args,
                                                                **kwargs)
        return super(PlayerEndpointMixin, self).dispatch(request,
                                                         *args,
                                                         **kwargs)


class PlayingStatusMixin(object):
    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data'):
            data = copy.copy(kwargs.get('data'))
            data['establishment'] = self.establishment.pk
            kwargs = copy.copy(kwargs)
            kwargs['data'] = data
        return super(PlayingStatusMixin, self).get_serializer(*args,
                                                              **kwargs)

    def get_object(self):
        return PlayerStatus.objects.get_or_create(
            establishment=self.establishment)[0]
