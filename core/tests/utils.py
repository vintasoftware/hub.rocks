# coding: utf-8

from django.test import TestCase, Client

from model_mommy import mommy


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self._user_password = 'test_pass'
        self.user = mommy.prepare('accounts.Account', username='test_username')
        self.user.set_password(self._user_password)
        self.user.save()
