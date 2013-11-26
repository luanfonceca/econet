#!/usr/bin/env python
# encoding: utf-8
u"""
models.py

Criado por Luan Fonseca em 08/08/2013.
"""

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from accounts.models import User

admin.site.register(User)