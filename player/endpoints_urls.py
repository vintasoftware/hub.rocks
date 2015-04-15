from django.conf.urls import patterns, include, url

from player.endpoints import SkipTrackAPIView, NowPlayingAPIView

urlpatterns = patterns('',
    url(r'^tracks/now-playing/skip/$',
        SkipTrackAPIView.as_view(), name='next'),
    url(r'^tracks/now-playing/$', NowPlayingAPIView.as_view(), name='now-playing'),
)
