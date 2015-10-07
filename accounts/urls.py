from django.conf.urls import patterns, url

from accounts.views import (AccountCreateView, WelcomeTemplateView,
                            UserLoginView, UserLogoutView)
urlpatterns = patterns('',
    url(r'^signup/$', AccountCreateView.as_view(), name='signup'),
    url(r'^welcome/$', WelcomeTemplateView.as_view(), name='welcome'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutView.as_view(), name='logout'),
)
