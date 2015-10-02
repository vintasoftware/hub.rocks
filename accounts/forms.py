# coding: utf-8

from django import forms

from accounts.models import Account


class AccountCreateForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name',
                  'password', 'password2', 'last_name']

    def __init__(self, *args, **kwargs):
        super(AccountCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean(self):
        cleaned_data = super(AccountCreateForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', "The two passwords don't match")

        return cleaned_data
