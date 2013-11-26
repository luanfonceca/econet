#!/usr/bin/env python
# encoding: utf-8
u"""
forms.py

Criado por Luan Fonseca em 08/08/2013.
"""

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (PasswordChangeForm, 
                                       SetPasswordForm,
                                       AuthenticationForm)

from accounts.models import *
from utils import HistoryModelForm

class UserForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)

        # FIXME: for now
        user.is_staff = True
        user.is_supervisor = True
        user.is_superuser = True
        
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        

class UserEditForm(HistoryModelForm):
    class Meta:
        model = User
        # fields = ['email', 'first_name', 'last_name']


class UserEditPasswordForm(PasswordChangeForm):
    class Meta:
        model = User


class UserResetPasswordForm(SetPasswordForm):
    class Meta:
        model = User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'login username-field',
            'placeholder': 'Nome de usuário',
            'autofocus': 'autofocus',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'login password-field',
            'placeholder': 'Senha'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password']
