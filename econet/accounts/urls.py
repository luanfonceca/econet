#!/usr/bin/env python
# encoding: utf-8
u"""
user.py

Criado por Luan Fonseca <luanfonceca@gmail.com> em 23/09/2013.
"""

from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^register/?$', 'register', name="registration_register"),
    url(r'^register/?$', 'register', name="auth_password_reset"),
    url(r'^login/?$', 'login', name="auth_login"),
   	url(r'^logout/?$', 'logout', name="auth_logout"),
   	
   	url(r'^profile/?$', 'profile', name="profile"),
)