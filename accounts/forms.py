# coding: utf-8

from django import forms

from django.contrib.auth.forms import AuthenticationForm


class RememberMeLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False,
                                     widget=forms.CheckboxInput())
