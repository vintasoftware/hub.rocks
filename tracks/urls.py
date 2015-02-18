from django.conf.urls import patterns, include, url

from tracks.views import VoteView, PlayerView


urlpatterns = patterns('',
    url(r'^$', VoteView.as_view(), name='vote'),
    url(r'^player/$', PlayerView.as_view(), name='vote'),
)
