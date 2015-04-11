from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy

from tracks.views import VoteView, PlayerView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(permanent=False,
                                    url=reverse_lazy(
                                        'tracks:vote',
                                        kwargs={'establishment': 'vinta'})),
                                    name='home'),
    url(r'^player/$', PlayerView.as_view(), name='player'),
    url(r'^(?P<establishment>\w+)/$', VoteView.as_view(), name='vote'),
)
