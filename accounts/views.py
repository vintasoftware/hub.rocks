# coding: utf-8

from django.views.generic import CreateView
from django.core.urlresolvers import reverse

from accounts.forms import AccountCreateForm


class AccountCreateView(CreateView):
    form_class = AccountCreateForm
    template_name = 'account/create.html'

    def get_success_url(self):
        url = reverse('tracks:vote', args=(self.object.username,))
        return url
