# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Producer.page_title'
        db.add_column('spares_producer', 'page_title', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Producer.meta_keywords'
        db.add_column('spares_producer', 'meta_keywords', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Producer.meta_description'
        db.add_column('spares_producer', 'meta_description', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Producer.page_title'
        db.delete_column('spares_producer', 'page_title')

        # Deleting field 'Producer.meta_keywords'
        db.delete_column('spares_producer', 'meta_keywords')

        # Deleting field 'Producer.meta_description'
        db.delete_column('spares_producer', 'meta_description')


    models = {
        'spares.producer': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Producer'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'spares.spare': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Spare'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('fields.AutoImageField', [], {'max_length': '100'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spares.Producer']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['spares']
