from django.conf.urls import patterns, include, url

from tracks.endpoints import (
    TrackListAPIView, VoteAPIView,
    NowPlayingAPIView, NextTrackAPIView,
    TrackDeleteAPIView)


urlpatterns = patterns('',
    url(r'^tracks/$', TrackListAPIView.as_view(), name='list'),
    url(r'^tracks/(?P<service_id>\d+)/vote/$', VoteAPIView.as_view(), name='vote'),
    
    url(r'^tracks/(?P<service_id>\d+)/now-playing/$', NowPlayingAPIView.as_view(), name='now-playing'),
    url(r'^tracks/next/$', NextTrackAPIView.as_view(), name='next'),
    url(r'^tracks/(?P<service_id>\d+)/$', TrackDeleteAPIView.as_view(), name='delete'),
)
