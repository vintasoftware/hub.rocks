# coding: utf-8

from django.views.generic import CreateView, TemplateView
from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin

from accounts.forms import AccountCreateForm


class AccountCreateView(CreateView):
    form_class = AccountCreateForm
    template_name = 'account/create.html'

    def get_success_url(self):
        return reverse('accounts:welcome')


class WelcomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'account/welcome.html'
