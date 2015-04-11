from django.conf.urls import patterns, include, url

from tracks.endpoints import (
    TrackListAPIView, VoteAPIView,
    NowPlayingAPIView, VoteSkipNowPlayingAPIView,
    SkipTrackAPIView)


urlpatterns = patterns('',
    url(r'^(?P<establishment>\w+)/tracks/$', TrackListAPIView.as_view(), name='list'),
    url(r'^(?P<establishment>\w+)/tracks/(?P<service_id>\d+)/vote/$', VoteAPIView.as_view(), name='vote'),
    
    url(r'^(?P<establishment>\w+)/tracks/now-playing/$', NowPlayingAPIView.as_view(), name='now-playing'),
    url(r'^(?P<establishment>\w+)/tracks/now-playing/voteskip/$', VoteSkipNowPlayingAPIView.as_view(),
        name='now-playing-skip'),
    url(r'^(?P<establishment>\w+)/tracks/now-playing/skip/$', SkipTrackAPIView.as_view(), name='next'),
)
