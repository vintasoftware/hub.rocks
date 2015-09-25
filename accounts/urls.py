from django.conf.urls import patterns, url

from accounts.views import AccountCreateView

urlpatterns = patterns('',
    url(r'^signup/$', AccountCreateView.as_view(), name='signup'),
)
