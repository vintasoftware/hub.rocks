# coding: utf-8

from django.views.generic import CreateView, TemplateView
from django.contrib import auth
from django.core.urlresolvers import reverse

from authtools.views import LoginView, LogoutView
from authtools.forms import UserCreationForm
from braces.views import LoginRequiredMixin

from accounts.forms import RememberMeLoginForm


class AccountCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'account/create.html'

    def get_success_url(self):
        return reverse('accounts:welcome')

    def form_valid(self, form):
        response = super(AccountCreateView, self).form_valid(form)
        new_user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'])

        auth.login(self.request, new_user)

        return response


class WelcomeTemplateView(TemplateView, LoginRequiredMixin):
    template_name = 'account/welcome.html'


class UserLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = RememberMeLoginForm
    expiry_age = 365 * 24 * 60 * 60

    def form_valid(self, form):
        result = super(UserLoginView, self).form_valid(form)
        if form.cleaned_data['remember_me']:
            self.request.session.set_expiry(self.expiry_age)
        return result

    def get_success_url(self):
        return reverse('tracks:vote', args=(self.request.user,))


class UserLogoutView(LogoutView):

    def get_redirect_url(self):
        return reverse('accounts:login')
