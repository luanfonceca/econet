#!/usr/bin/env python
# encoding: utf-8
u"""
models.py

Criado por Luan Fonseca <luanfonceca@gmail.com> em 23/09/2013.
"""

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        _now = now()
        if not email:
            raise ValueError(_(u'The given email must be set.'))
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=True,
            is_active=True,
            is_superuser=False,
            last_login=_now,
            created_at=_now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email,
            password,
            **extra_fields
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=_(u'Nome')
    )
    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=_(u'Sobrenome')
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name=_(u'Email')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_(u'Administrador')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_(u'Esta Ativo')
    )
    is_manager = models.BooleanField(
        default=False,
        verbose_name=_(u'Marque caso este usuário seja um Gestor.')
    )

    # Django Managers
    objects = UserManager()

    # Configs
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = _(u'Perfil')
        verbose_name_plural = _(u'Perfis')

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    @property
    def full_name(self):
        if self.first_name and last_name:
            return u"%s %s" % (self.first_name, self.last_name)
        else:
            return u"%s" % self.email.split("@")[0]
