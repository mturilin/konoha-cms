# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Page.style'
        db.delete_column(u'konoha_page', 'style')

        # Deleting field 'Page.published'
        db.delete_column(u'konoha_page', 'published')


        # Deleting column for 'Page.published_version' to match new field type.
        db.delete_column(u'konoha_page', 'published_version')


        # Changing field 'Page.data'
        db.alter_column(u'konoha_page', 'data', self.gf('django.db.models.fields.TextField')())

        # Deleting field 'Page.template'
        db.delete_column(u'konoha_page', 'template')

        # Deleting field 'PageVersion.published'
        db.delete_column(u'konoha_pageversion', 'published')

        # Deleting field 'PageVersion.style'
        db.delete_column(u'konoha_pageversion', 'style')

        # Deleting field 'PageVersion.template'
        db.delete_column(u'konoha_pageversion', 'template')


        # Changing field 'PageVersion.user'
        db.alter_column(u'konoha_pageversion', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['studentoffice.CustomUser'], null=True))

        # Changing field 'PageVersion.data'
        db.alter_column(u'konoha_pageversion', 'data', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):
        # Removing index on 'Page', fields ['published_version']
        db.delete_index(u'konoha_page', ['published_version_id'])

        # Adding field 'Page.style'
        db.add_column(u'konoha_page', 'style',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.published'
        db.add_column(u'konoha_page', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Renaming column for 'Page.published_version' to match new field type.
        db.rename_column(u'konoha_page', 'published_version_id', 'published_version')
        # Changing field 'Page.published_version'
        db.alter_column(u'konoha_page', 'published_version', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Page.data'
        db.alter_column(u'konoha_page', 'data', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Page.template'
        db.alter_column(u'konoha_page', 'template', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding field 'PageVersion.published'
        db.add_column(u'konoha_pageversion', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'PageVersion.style'
        db.add_column(u'konoha_pageversion', 'style',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PageVersion.template'
        db.add_column(u'konoha_pageversion', 'template',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PageVersion.user'
        raise RuntimeError("Cannot reverse this migration. 'PageVersion.user' and its values cannot be restored.")

        # Changing field 'PageVersion.data'
        db.alter_column(u'konoha_pageversion', 'data', self.gf('django.db.models.fields.TextField')(null=True))

    models = {
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
        },
        'filer.folder': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Folder'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filer_owned_folders'", 'null': 'True', 'to': u"orm['studentoffice.CustomUser']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'konoha.page': {
            'Meta': {'object_name': 'Page'},
            'container': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'inner_pages'", 'null': 'True', 'to': u"orm['konoha.Page']"}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'text/html'", 'max_length': '100'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_folder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Folder']", 'null': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'published_version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['konoha.PageVersion']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'konoha.pageversion': {
            'Meta': {'unique_together': "(('page', 'version'),)", 'object_name': 'PageVersion'},
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'error': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': u"orm['konoha.Page']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentoffice.CustomUser']", 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'studentoffice.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        }
    }

    complete_apps = ['konoha']