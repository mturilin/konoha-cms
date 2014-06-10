# -*- coding: utf-8 -*-
from datetime import datetime
from south.db import db
from south.v2 import DataMigration
from konoha import KonohaError
from django.db.models import Max
import yaml
from konoha import KonohaError



class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        def page_last_version(page):
            """ Gets last saved PageVersion object of a page """
            version = page.versions.aggregate(Max('version'))['version__max']

            if version is not None:
                return page.versions.get(version=version)

            return None

        def publish(page):
            page_version = page_last_version(page)
            if not page_version:
                raise KonohaError("There are no versions to publish")

            assert isinstance(page_version, orm.PageVersion)

            if page_version.valid:
                page.published_version = page_version
                page.save()
            else:
                raise KonohaError("Can't publish non-valid version")

        course_detailt1 = (
            'cource_voip_free',
            'course_asterisk',
            'course_asterisk_business',
            'course_ccna_bootcamp',
            'course_ccna_discovery',
            'course_ccna_exploration',
            'course_ccna_rs',
            'course_ccna_rs_intensive',
            'course_ccna_security',
            'course_ccnp',
            'course_ccnp_route',
            'course_ccnp_switch',
            'course_cisco_asa',
            'course_cisco_mpls',
            'course_cisco_network_engineer',
            'course_cisco_presale',
            'course_cisco_voip',
            'course_cisco_vpn',
            'course_cisco_zbf',
            'course_ip_telephony',
            'course_itil',
            'course_linux_administration',
            'course_mcsa',
            'course_microsoft_free',
            'course_mssql_administrating',
            'course_mssql_data_warehouse',
            'course_mssql_querying',
            'course_oracle_11g',
            'course_oracle_12c',
            'course_redhat_linux',
            'course_start_cisco',
            'course_vmware_begginer',
            'course_vmware_free',
            'course_vmware_pro',
            'course_windows_server_administering',
            'course_windows_server_administrator',
            'course_windows_server_advanced_configuring',
            'course_windows_server_installing')
        for page in orm.Page.objects.filter(name__in=course_detailt1):
            page.template = 'skillfactoryru/konoha/course_detail.html'
            page.save()
            publish(page)
        #
        page = orm.Page.objects.get(name='index')
        page.template = 'skillfactoryru/konoha/index.html'
        page.save()
        publish(page)
        #
        page = orm.Page.objects.get(name='faq')
        page.template = 'skillfactoryru/konoha/faq.html'
        page.save()
        publish(page)
        #
        page = orm.Page.objects.get(name='how_it_works')
        page.template = 'skillfactoryru/konoha/how_it_works.html'
        page.save()
        publish(page)
        #
        page = orm.Page.objects.get(name='reviews')
        page.template = 'skillfactoryru/konoha/reviews.html'
        page.save()
        publish(page)
        #
        page = orm.Page.objects.get(name='courses')
        page.template = 'skillfactoryru/konoha/courses.html'
        page.save()
        publish(page)

        page = orm.Page.objects.get(name='free_courses')
        page.template = 'skillfactoryru/konoha/courses.html'
        page.save()
        publish(page)

        for page in orm.Page.objects.filter(name__in=('contract_offer', 'info_cisco_academy_qap',
                                                      'info_confidentiality_policy', 'info_contacts',
                                                      'info_getccna_skillfactory', 'corporate_discount',
                                                      'ccna-spring-promo', 'signup_ok')):
            page.template = 'skillfactoryru/konoha/content_page.html'
            page.save()
            publish(page)

        ### Прописываем файлы и картинки
        def item_handler(item):
            if isinstance(item, (str, unicode)):
                try:
                    if page.image_folder.all_files.filter(name=item).count() > 0:
                        return str(page.image_folder.all_files.filter(name=item)[0].file.url)
                    elif page.image_folder.all_files.filter(original_filename=item).count() > 0:
                        return str(page.image_folder.all_files.filter(original_filename=item)[0].file.url)
                except:
                    pass
                #try:
                #    file_query = page.image_folder.all_files.filter(original_filename=item)
                #    file = file_query[0]
                #    return str(file.file.url)
                #except Exception as e:
                #    print e
            elif isinstance(item, (dict, list)):
                recursion_fn(item)

        def recursion_fn(data):
            if isinstance(data, dict):
                for key, value in data.iteritems():
                    new_item = item_handler(data[key])
                    if new_item:
                        data[key] = new_item
            elif isinstance(data, list):
                for i in xrange(len(data)):
                    new_item = item_handler(data[i])
                    if new_item:
                        data[i] = new_item

        for page in orm.Page.objects.all():
            d = yaml.load(page.data)
            recursion_fn(d)
            page.data = yaml.dump(d, encoding='UTF-8', allow_unicode=True, default_flow_style=False)
            version_query = page.versions
            if version_query.count() == 0:
                version = 1
            else:
                version = version_query.aggregate(Max('version'))['version__max'] + 1
            new_version = page.versions.create(page=page, data=page.data, valid=True, error='', date_created=datetime.now(), version=version)
            page.published_version = new_version
            page.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("Cannot reverse this migration.")

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
        'filer.clipboard': {
            'Meta': {'object_name': 'Clipboard'},
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'in_clipboards'", 'symmetrical': 'False', 'through': "orm['filer.ClipboardItem']", 'to': "orm['filer.File']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filer_clipboards'", 'to': u"orm['studentoffice.CustomUser']"})
        },
        'filer.clipboarditem': {
            'Meta': {'object_name': 'ClipboardItem'},
            'clipboard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Clipboard']"}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.File']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'filer.file': {
            'Meta': {'object_name': 'File'},
            '_file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'all_files'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_files'", 'null': 'True', 'to': u"orm['studentoffice.CustomUser']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_filer.file_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.folder': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Folder'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filer_owned_folders'", 'null': 'True', 'to': u"orm['studentoffice.CustomUser']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.folderpermission': {
            'Meta': {'object_name': 'FolderPermission'},
            'can_add_children': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'can_edit': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'can_read': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'everybody': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Folder']", 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filer_folder_permissions'", 'null': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filer_folder_permissions'", 'null': 'True', 'to': u"orm['studentoffice.CustomUser']"})
        },
        'filer.image': {
            'Meta': {'object_name': 'Image', '_ormbases': ['filer.File']},
            '_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'default_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['filer.File']", 'unique': 'True', 'primary_key': 'True'}),
            'must_always_publish_author_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'must_always_publish_copyright': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'konoha.page': {
            'Meta': {'object_name': 'Page'},
            'container': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'inner_pages'", 'null': 'True', 'to': u"orm['konoha.Page']"}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'text/html'", 'max_length': '100'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'image_folder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Folder']", 'null': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'published_version': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['konoha.PageVersion']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
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

    complete_apps = ['filer', 'konoha']
    symmetrical = True
