#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from app.views.site import *
from app.views.bounty import *
from app.views import collect_spot

urlpatterns = patterns('',
    url(regex=r'^$', view=HomeView.as_view(), name='home'),
    url(r'^about_us$', TemplateView.as_view(template_name="site/about_us.html"), name="about_us"),
    
    url(r'^collect_spots/create/?$', view=collect_spot.create, name="collect_spot_create"),
    url(r'^collect_spots/get_json/?$', view=collect_spot.get_json, name="collect_spot_json"),

    url(
        regex=r'^bounty/create/$',
        view=BountyCreateView.as_view(),
        name='bounty_create'
    ),
    url(
        regex=r'^bounty/$',
        view=BountyListView.as_view(),
        name='bounty_list'
    ),
    url(
        regex=r'^bounty/(?P<pk>\d+?)/$',
        view=BountyDetailView.as_view(),
        name='bounty_detail'
    ),
    url(
        regex=r'^bounty/(?P<pk>\d+?)/update/$',
        view=BountyUpdateView.as_view(),
        name='bounty_update'
    ),
    url(
        regex=r'^bounty/(?P<pk>\d+?)/delete/$',
        view=BountyDeleteView.as_view(),
        name='bounty_delete'
    ),
    
    url(r'^spot/(?P<pk>\d+?)/descart/item/?$', view=collect_spot.descart_item, name="descart_item"),
)
