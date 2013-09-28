#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="site/home.html"), name="home"),
    url(r'^about_us$', TemplateView.as_view(template_name="site/about_us.html"), name="about_us"),
)
