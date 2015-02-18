from django.conf.urls import patterns, include, url

from tracks.endpoints import (
    TracksAPIView, VoteAPIView,
    NowPlayingAPIView)


urlpatterns = patterns('',
    url(r'^tracks/$', TracksAPIView.as_view(), name='tracks'),
    url(r'^tracks/(?P<service_id>\d+)/vote/$', VoteAPIView.as_view(), name='vote'),
    url(r'^tracks/(?P<service_id>\d+)/now-playing/$', NowPlayingAPIView.as_view(), name='vote'),
)
