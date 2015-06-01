
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

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
