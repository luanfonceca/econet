#!/usr/bin/env python
# encoding: utf-8
u"""
models.py

Criado por Luan Fonseca <luanfonceca@gmail.com> em 23/09/2013.
"""

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

# Registrando todas os Models da app na Admin.
map(lambda x:
	admin.site.register(
		x.model_class()
	) if x.model_class() else None, 
	ContentType.objects.filter(app_label=__package__)
)
	