from django.conf.urls import patterns, include, url

from player.endpoints import SkipTrackAPIView

urlpatterns = patterns('',
    url(r'^tracks/now-playing/skip/$',
        SkipTrackAPIView.as_view(), name='next'),
)
