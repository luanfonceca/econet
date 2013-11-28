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

from accounts.models import User

class Timeline(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(null=False, max_length=50)
    entity = models.CharField(null=False, max_length=50)
    description = models.TextField(
        verbose_name=u'Descrição', 
        blank=True,
    )

    # relations
    user = models.ForeignKey(
        to='accounts.User',
        related_name='timeline',
        verbose_name=u'Usuario',
        null=True, blank=True
    )        

    class Meta:
        verbose_name = u'Atualização'
        verbose_name_plural = u'Atualizações'
        ordering = ['-created_at']


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
    local = models.CharField(
        verbose_name=u'Local', 
        max_length=50,
        help_text=u'Departamento, Região, Bloco ou Ponto de Referência.',
        null=True,
        blank=True
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

    @property
    def pretty_itens(self):
        return ', '.join(self.accepted_itens.values('name'))
        

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

@receiver(post_save, sender=CollectSpot)
@receiver(post_save, sender=Item)
@receiver(post_save, sender=User)
def update_timeline(**kwargs):
    obj = kwargs.get('instance')
    entity = kwargs.get('sender')._meta.verbose_name
    user = None
    description = None

    if kwargs.get('created'):
        if isinstance(obj, CollectSpot):
            action = u'Criação do %s' % entity   
            try:
                user = obj.collectors.latest('id')
            except User.DoesNotExist:
                pass

            description = u'''
            %(action)s, chamado "%(cs_name)s"
            na localidade: %(local)s. 
            Que está apto à receber: %(pretty_itens)s.
            ''' % {
                'cs_name': obj.name or u'Sem nome',
                'user': user or u'Sem usuário',
                'action': action,
                'entity': entity,
                'local': obj.local or u'Sem localidade',
                'pretty_itens': obj.pretty_itens or u'Sem itens'
            }
        elif isinstance(obj, Item):
            action = u'Criação de um %s' % entity   
            description = u'''
            %(action)s, chamado "%(item_name)s".
            ''' % {
                'action': action,
                'item_name': obj.name or 'Sem nome',
            }
        elif isinstance(obj, User):
            user = obj
            action = u'Criação de um %s' % entity
            description = u'''
            %(action)s, chamado <strong>"%(user_name)s</strong>".
            ''' % {
                'action': action,
                'user_name': obj.get_full_name() or obj.email,
            }

        Timeline.objects.create(
            user=user,
            action=action,
            entity=entity,
            description=description
        )