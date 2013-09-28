#!/usr/bin/env python
# encoding: utf-8

from django import template
from django.template import Context, loader, Template

register = template.Library()

@register.simple_tag
def is_active_tab(url, tab, cls=None):
    """
    Usage:
        In your Master Template:
            <ul class="nav navbar-nav">
              <li {% is_active_tab 'about_us' tab %}>
                  <a href="{% url 'about_us' %}">About us</a>
              </li>
            </ul>

        In your template:
            {% include "site/menu.html" with tab='about_us' %}

    url :: Is the Name that you want to use to refer your page
    tab :: Is the Name that pass when you include the menu
    cls :: Is the Classes which your <li> shoud have
    """
    template = Template('')
    context = Context({
        'cls': cls or '',
        'is_active': 'active' if url == tab else ''
    })
    if any([url, tab, cls]):
        template = Template("class=\"{{ is_active }}{{ cls }}\"")
    return template.render(context)