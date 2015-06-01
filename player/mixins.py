
import logging

import time
import pylast

from django.conf import settings

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


class LastFMScrobblerMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and settings.LASTFM_API_KEY:
            self.network = pylast.LastFMNetwork(
                api_key=settings.LASTFM_API_KEY,
                api_secret=settings.LASTFM_API_SECRET,
                username=request.user.lastfm_username,
                password_hash=request.user.lastfm_hashed_password)
        return super(LastFMScrobblerMixin, self).dispatch(request, *args,
                                                          **kwargs)

    def scrobble(self, artist, title, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        if settings.LASTFM_API_KEY and self.establishment.lastfm_username:
            self.network.scrobble(artist=artist, title=title,
                                  timestamp=timestamp)
        else:
            logging.info("last.fm not setup, would scrobble {} for {}".format(
                         title, self.establishment.username))
