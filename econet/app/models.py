#!/usr/bin/env python
# encoding: utf-8
u"""
models.py

Criado por Luan Fonseca em 18/10/2013.
"""

from django.db import models
from django.db.models.signals import *
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField


class Bounty(models.Model):
    name = models.CharField(
        verbose_name=u'Nome', 
        max_length=50
    )
    slug = AutoSlugField(
        populate_from='name', 
        separator='_',
        max_length=100, 
        unique=True, 
        overwrite=True
    )
    description = models.TextField(
        verbose_name=u'Descrição'
    )
    value = models.CharField(
        verbose_name=u'Valor', 
        max_length=50
    )

    # relations
    users = models.ManyToManyField(
        to='accounts.User',
        related_name='bounties',
        verbose_name=u'Usuários',
        blank=True
    )
    class Meta:
        verbose_name = 'Recompença'
        verbose_name_plural = 'Recompenças'

    @models.permalink
    def get_absolute_url(self):
        return ('bounty_detail', [self.pk])
    
    

class Item(models.Model):
    name = models.CharField(
        verbose_name=u'Nome', 
        max_length=50
    )
    slug = AutoSlugField(
        populate_from='name', 
        separator='_',
        max_length=100, 
        unique=True, 
        overwrite=True
    )

    # relations
    bounties = models.ManyToManyField(
        to='app.Bounty',
        related_name='itens',
        verbose_name=u'Recompenças',
        blank=True, null=True
    )
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

    def __unicode__(self):
        return unicode(self.name)
    

class CollectSpot(models.Model):
    name = models.CharField(
        verbose_name=u'Nome', 
        max_length=50
    )
    description = models.TextField(
        verbose_name=u'Descrição', 
        blank=True,
    )
    latitude = models.CharField(
        verbose_name=u'Latitude', 
        max_length=50
    )
    longitude = models.CharField(
        verbose_name=u'Longitude', 
        max_length=50
    )
    slug = AutoSlugField(
        populate_from='name', 
        separator='_',
        max_length=100, 
        unique=True, 
        overwrite=True
    )

    # relations
    collectors = models.ManyToManyField(
        to='accounts.User', 
        related_name='collect_spots',
        verbose_name=u'Colletores',
    )
    accepted_itens = models.ManyToManyField(
        to='app.Item', 
        related_name='collect_spots',
        verbose_name=u'Itens Aceitos',
        blank=True,
    )
    class Meta:
        verbose_name = 'Ponto de Coleta'
        verbose_name_plural = 'Pontos de Coleta'


class DescartedItem(models.Model):
    amount = models.CharField(
        max_length=150, 
        null=True, 
        blank=True, 
        verbose_name=u'Quantidade'
    )

    # relations 
    check_in = models.ForeignKey(
        to='app.CheckIn',
        related_name='descarted_itens', 
        verbose_name=u'Check-In',
    )
    item = models.ForeignKey(
        to='app.Item',
        related_name='descarted_itens', 
        verbose_name=u'Item',
    )

    class Meta:
        verbose_name = 'Item Descartado'
        verbose_name_plural = 'Itens Descartados'
    

class CheckIn(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    # relations
    user = models.ForeignKey(
        to='accounts.User',
        related_name='check_ins',
        verbose_name=u'Usuario'
    )
    collect_spot = models.ForeignKey(
        to='app.CollectSpot',
        related_name='check_ins',
        verbose_name=u'Ponto de Coleta',
    )
    itens = models.ManyToManyField(
        to='app.Item',
        through='app.DescartedItem',
        null=True, 
        blank=True, 
        related_name='check_ins',
        verbose_name=u'Itens'
    )
    bounties = models.ManyToManyField(
        to='app.Bounty', 
        related_name='check_ins',
        verbose_name=u'Recompenças',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Check-In'
        verbose_name_plural = 'Check-Ins'

    def __unicode__(self):
        return u"%s - %s" % (
            self.collect_spot.name, 
            ', '.join(self.itens.values_list('name', flat=True)) or 'Nenhum Item'
        )