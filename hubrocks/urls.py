from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('tracks.urls', namespace='tracks')),
    url(r'^api/', include('tracks.endpoints_urls', namespace='api')),
)
