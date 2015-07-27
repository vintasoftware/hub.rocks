from django.conf.urls import patterns, url

from tracks.endpoints import (
    TrackListAPIView, VoteAPIView,
    VoteSkipNowPlayingAPIView, InsertTrackAPIView, PlayingStatusAPIView)


urlpatterns = patterns('',
    url(r'^tracks/$', TrackListAPIView.as_view(), name='list'),
    url(r'^tracks/(?P<track_id>\d+)/vote/$', VoteAPIView.as_view(),
        name='vote'),

    url(r'^tracks/now-playing/voteskip/$', VoteSkipNowPlayingAPIView.as_view(),
        name='now-playing-skip'),
    url(r'^tracks/(?P<service>.+)/(?P<service_id>.+)/$',
        InsertTrackAPIView.as_view(), name='insert'),
    url(r'tracks/change-player-status/$', PlayingStatusAPIView.as_view(),
        name='change-player-status'),
)
