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
        verbose_name=u'Recompenças'
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
        related_name='check_ins',
        verbose_name=u'Itens',
    )
    bounties = models.ManyToManyField(
        to='app.Bounty', 
        related_name='check_ins',
        verbose_name=u'Recompenças',
    )
    class Meta:
        verbose_name = 'Check-In'
        verbose_name_plural = 'Check-Ins'


@receiver(post_save, sender=CollectSpot)
def append_itens_to_descriptions(**kwargs):
    obj = kwargs.get('instance')
    update_fields = kwargs.get('update_fields') or []
    if kwargs.get('created') or \
       'accepted_itens' in update_fields:
        obj.description = map(
            lambda x: '\nItem Aceito: %s' % x,
            obj.accepted_itens.values_list('name', flat=True)
        )
        obj.save()