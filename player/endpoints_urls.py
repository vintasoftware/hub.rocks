from django.conf.urls import patterns, url

from player.endpoints import (SkipTrackAPIView, NowPlayingAPIView,
                              PlayingStatusAPIView)

urlpatterns = patterns('',
    url(r'^tracks/now-playing/skip/$',
        SkipTrackAPIView.as_view(), name='next'),
    url(r'^tracks/now-playing/$', NowPlayingAPIView.as_view(),
        name='now-playing'),
    url(r'^player/change-status/$', PlayingStatusAPIView.as_view(),
        name='change-status'),
)
