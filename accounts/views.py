# coding: utf-8

from django.views.generic import CreateView, TemplateView
from django.core.urlresolvers import reverse

from authtools.views import LoginView, LogoutView
from braces.views import LoginRequiredMixin

from accounts.forms import AccountCreateForm


class AccountCreateView(CreateView):
    form_class = AccountCreateForm
    template_name = 'account/create.html'

    def get_success_url(self):
        return reverse('accounts:welcome')


class WelcomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'account/welcome.html'


class UserLoginView(LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse('tracks:vote', args=(self.request.user,))


class UserLogoutView(LogoutView):

    def get_redirect_url(self):
        return reverse('accounts:login')
