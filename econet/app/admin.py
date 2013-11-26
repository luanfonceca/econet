#!/usr/bin/env python
# encoding: utf-8
u"""
models.py

Criado por Luan Fonseca em 23/10/2013.
"""

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from app.models import CheckIn, Item, CollectSpot

admin.site.register(CheckIn)
admin.site.register(Item)
admin.site.register(CollectSpot)
