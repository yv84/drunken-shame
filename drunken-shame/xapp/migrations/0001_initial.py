# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table('xapp_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('spots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('xapp', ['Room'])

        # Adding model 'User'
        db.create_table('xapp_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('paycheck', self.gf('django.db.models.fields.IntegerField')()),
            ('date_joined', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('xapp', ['User'])


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table('xapp_room')

        # Deleting model 'User'
        db.delete_table('xapp_user')


    models = {
        'xapp.room': {
            'Meta': {'object_name': 'Room'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {})
        },
        'xapp.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['xapp']