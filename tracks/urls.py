from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy

from tracks.views import VoteView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(permanent=False,
                                    url=reverse_lazy(
                                        'tracks:vote',
                                        kwargs={'establishment': 'vinta'})),
        name='home'),
    url(r'^(?P<establishment>[\w.@+-]+)/$', VoteView.as_view(), name='vote'),
)
