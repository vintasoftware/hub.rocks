from django.conf.urls import patterns, url

from tracks.endpoints import (
    VoteAPIView, VoteSkipNowPlayingAPIView, ListCreateTrackAPIView,
    PlayingStatusAPIView)


urlpatterns = patterns('',
    url(r'^tracks/(?P<track_id>\d+)/vote/$', VoteAPIView.as_view(),
        name='vote'),

    url(r'^tracks/now-playing/voteskip/$', VoteSkipNowPlayingAPIView.as_view(),
        name='now-playing-skip'),
    url(r'^tracks/$', ListCreateTrackAPIView.as_view(), name='list-create'),
    url(r'^tracks/change-player-status/$', PlayingStatusAPIView.as_view(),
        name='change-status'),
)
