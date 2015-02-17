from django.conf.urls import patterns, include, url

from tracks.endpoints import VoteAPIView


urlpatterns = patterns('',
    url(r'^tracks/(?P<service_id>\d+)/vote/$', VoteAPIView.as_view(), name='vote'),
)
