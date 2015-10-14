from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy

from tracks.views import VoteView, HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^(?P<establishment>[\w.@+-]+)/$', VoteView.as_view(), name='vote'),
)
