from django.conf.urls import patterns, url

from accounts.views import AccountCreateView, WelcomeTemplateView

urlpatterns = patterns('',
    url(r'^signup/$', AccountCreateView.as_view(), name='signup'),
    url(r'^welcome/$', WelcomeTemplateView.as_view(), name='welcome'),
)
