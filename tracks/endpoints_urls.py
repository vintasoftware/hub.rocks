from django.conf.urls import patterns, url

from tracks.endpoints import (
    TrackListAPIView, VoteAPIView,
    VoteSkipNowPlayingAPIView)


urlpatterns = patterns('',
    url(r'^tracks/$', TrackListAPIView.as_view(), name='list'),
    url(r'^tracks/(?P<service_id>.+)/vote/$', VoteAPIView.as_view(),
        name='vote'),

    url(r'^tracks/now-playing/voteskip/$', VoteSkipNowPlayingAPIView.as_view(),
        name='now-playing-skip'),
)
