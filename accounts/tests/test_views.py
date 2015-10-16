# coding: utf-8

from django.test import TestCase, Client

from django.core.urlresolvers import reverse
from django.utils.six.moves import http_client

from core.tests.utils import BaseTestCase
from accounts.models import Account


class AccountCreateViewTest(TestCase):
    view_name = 'accounts:signup'

    def setUp(self):
        self.client = Client()
        self.url = reverse(self.view_name)
        self.params = {
            'first_name': 'first_name_test',
            'last_name': 'last_name_test',
            'email': 'email_test@email.com',
            'password1': 'pass_test',
            'password2': 'pass_test',
            'username': 'station_name_test'
        }

    def test_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, http_client.OK)

    def test_creates_a_new_account(self):
        self.client.post(self.url, data=self.params)
        self.assertEqual(Account.objects.all().count(), 1)


class LoginViewTest(BaseTestCase):
    view_name = 'accounts:login'

    def setUp(self):
        super(LoginViewTest, self).setUp()
        self.url = reverse(self.view_name)
        self.params = {
            'username': 'test_username',
            'password': 'test_pass'
        }

    def test_get(self):
        response = self.client.get(self.url)

        self.assertIn('form', response.context_data)

    def test_post_login(self):
        response = self.client.post(self.url, self.params, follow=True)

        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.user)
