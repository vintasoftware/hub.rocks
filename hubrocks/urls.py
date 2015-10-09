from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('authtools.urls')),

    url(r'^', include('accounts.urls', namespace='accounts')),
    url(r'^', include('player.urls', namespace='player')),
    url(r'^', include('tracks.urls', namespace='tracks')),
    url(r'^api/', include('player.endpoints_urls', namespace='api-player')),
    url(r'^api/(?P<establishment>[\w.@+-]+)/', include('tracks.endpoints_urls',
        namespace='api')),
)
