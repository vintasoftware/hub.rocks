
from django.conf.urls import patterns, url

from player.views import PlayerView

urlpatterns = patterns('',
    url(r'^player/$', PlayerView.as_view(), name='player'),
)
