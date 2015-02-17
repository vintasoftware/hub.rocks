from django.conf.urls import patterns, include, url

from tracks.views import VoteView


urlpatterns = patterns('',
    url(r'^$', VoteView.as_view(), name='vote'),
)
