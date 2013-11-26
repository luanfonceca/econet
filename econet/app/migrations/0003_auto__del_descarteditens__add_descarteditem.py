# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DescartedItens'
        db.delete_table(u'app_descarteditens')

        # Adding model 'DescartedItem'
        db.create_table(u'app_descarteditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('check_in', self.gf('django.db.models.fields.related.ForeignKey')(related_name='descarted_itens', to=orm['app.CheckIn'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='descarted_itens', to=orm['app.Item'])),
        ))
        db.send_create_signal(u'app', ['DescartedItem'])


    def backwards(self, orm):
        # Adding model 'DescartedItens'
        db.create_table(u'app_descarteditens', (
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='descarted_itens', to=orm['app.Item'])),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('check_in', self.gf('django.db.models.fields.related.ForeignKey')(related_name='descarted_itens', to=orm['app.CheckIn'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'app', ['DescartedItens'])

        # Deleting model 'DescartedItem'
        db.delete_table(u'app_descarteditem')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_colector': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'app.bounty': {
            'Meta': {'object_name': 'Bounty'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '100', 'separator': "'_'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'bounties'", 'blank': 'True', 'to': u"orm['accounts.User']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'app.checkin': {
            'Meta': {'object_name': 'CheckIn'},
            'bounties': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'check_ins'", 'symmetrical': 'False', 'to': u"orm['app.Bounty']"}),
            'collect_spot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'check_ins'", 'to': u"orm['app.CollectSpot']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itens': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'check_ins'", 'to': u"orm['app.Item']", 'through': u"orm['app.DescartedItem']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'check_ins'", 'to': u"orm['accounts.User']"})
        },
        u'app.collectspot': {
            'Meta': {'object_name': 'CollectSpot'},
            'accepted_itens': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'collect_spots'", 'blank': 'True', 'to': u"orm['app.Item']"}),
            'collectors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'collect_spots'", 'symmetrical': 'False', 'to': u"orm['accounts.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '100', 'separator': "'_'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'True'})
        },
        u'app.descarteditem': {
            'Meta': {'object_name': 'DescartedItem'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'check_in': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'descarted_itens'", 'to': u"orm['app.CheckIn']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'descarted_itens'", 'to': u"orm['app.Item']"})
        },
        u'app.item': {
            'Meta': {'object_name': 'Item'},
            'bounties': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'itens'", 'symmetrical': 'False', 'to': u"orm['app.Bounty']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '100', 'separator': "'_'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']