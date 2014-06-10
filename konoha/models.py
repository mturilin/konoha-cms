# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from coffin.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.conf import settings
from django.db.models import Max
from django.http import HttpRequest
from django.template import RequestContext
from jinja2.exceptions import TemplateError
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from filer.fields.folder import FilerFolderField
import yaml
from yaml.error import YAMLError
from konoha import KonohaError


try:
    from django_tools.middlewares.ThreadLocal import get_current_user, get_current_request
except ImportError:
    get_current_user = lambda: None


class ChoiceFilerFolderField(FilerFolderField):
    def __init__(self, **kwargs):
        super(ChoiceFilerFolderField, self).__init__(**kwargs)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {
            'form_class': forms.ModelChoiceField,
            # 'rel': self.rel,
        }
        defaults.update(kwargs)
        return super(FilerFolderField, self).formfield(**defaults)


class PageManager(models.Manager):
    def by_path(self, path):
        '''
        Geting page using caching
        '''
        return self.get(path=path)

    def by_name(self, name):
        '''
        Geting page using caching
        '''
        return self.get(name=name)

    def exists_with_name(self, name):
        return self.filter(name=name).exists()

    def exists_with_path(self, path):
        return self.filter(path=path).exists()


class Page(MPTTModel):
    container = TreeForeignKey('self', related_name='inner_pages', null=True, blank=True)

    name = models.CharField(max_length=100, db_index=True, unique=True)
    path = models.CharField(max_length=255, db_index=True, null=True, blank=True, unique=True)
    data = models.TextField(blank=True, null=False, default="")
    template = models.CharField(max_length=1000, blank=True, null=True)

    #image_folder = ChoiceFilerFolderField(null=True)

    published_version = models.ForeignKey("PageVersion", null=True, blank=True, related_name='+')

    login_required = models.BooleanField(default=False)

    content_type = models.CharField(max_length=100, default="text/html")

    class MPTTMeta:
        parent_attr = 'container'
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.path.startswith('/'):
            raise ValidationError({
                'path':["Path should not start with slash"]
            })
        return super(Page, self).clean_fields(exclude)


    @property
    def full_path(self):
        return "%s/%s" % (settings.KONOHA_ROOT, self.path)

    def get_absolute_url(self):
        request = get_current_request()
        if request:
            return "%s://%s%s" % ('https' if request.is_secure() else 'http', request.get_host(), self.full_path)
        else:
            return self.full_path

    @property
    def content_type_with_charset(self):
        return "%s; charset=%s" % (self.content_type, settings.DEFAULT_CHARSET)

    @property
    def published_data(self):
        """
        @returns Data field of the published version. Throws error if the page is not published.
        """
        if not self.published_version:
            raise KonohaError("Page is not published")

        return self.published_version.data

    @property
    def published(self):
        return bool(self.published_version)

    def version_data(self, version):
        """
        @returns Data field of the provided version.
        """
        data = self.versions.get(version=version).data
        return data

    def save(self, *args, **kwargs):
        """
        Saves the page and creates a new version if 'data' was changed
        """
        super(Page, self).save()
        if 'data' in kwargs.get('updated_fields', set()) or not self.latest_version or self.data != self.latest_version.data:
            self._save_new_version()


    @property
    def latest_version(self):
        """ Gets last saved PageVersion object of a page """
        version = self.versions.aggregate(Max('version'))['version__max']

        if version is not None:
            return self.versions.get(version=version)

        return None

    def publish(self, page_version=None):
        """ Publishes a version saving versionized fields in 'Page' instance and setting up 'published_version'. Also sets up 'published' flag in 'konoha_pageversion' table. """
        page_version = page_version or self.latest_version
        if not page_version:
            raise KonohaError("There are no versions to publish")

        assert isinstance(page_version, PageVersion)

        if page_version.valid:
            self.published_version = page_version
            self.save()
        else:
            raise KonohaError("Can't publish non-valid version")

    def unpublish(self):
        self.published_version = None
        self.save()

    def clean_versions(self):
        # remove the oldest version if needed
        num_versions = self.versions.count()
        if num_versions > 0:
            oldest_version = self.versions.order_by('version')[0]

            oldest_version_date_created = oldest_version.date_created
            oldest_version_id = oldest_version.id

            max_versions_num = getattr(settings, "MAX_VERSIONS_NUM", 100)
            max_versions_period = getattr(settings, "MAX_VERSIONS_PERIOD", 30)
            if num_versions > max_versions_num and oldest_version_date_created < datetime.now() - timedelta(
                    days=max_versions_period):
                oldest_version_version = oldest_version.version
                assert oldest_version_version != self.published_version, "Attempt to delete the currently published version"

                PageVersion.objects.filter(id=oldest_version_id).delete()

    def _save_new_version(self):
        """ Saves a page and creates a new version of a page """
        # create a new page version
        new_version = self.versions.create(page=self, data=self.data)

        self.clean_versions()

        return new_version

    objects = PageManager()


class PageVersion(models.Model):
    """ This is a page version abstraction. Every page can have one or more versions.
    Only 'template', 'data' and 'style' fields are included in the version. Others are in the 'Page' class. """

    class Meta:
        unique_together = (('page', 'version'))

    page = models.ForeignKey(Page, related_name='versions')
    version = models.IntegerField(null=False, default=0)

    date_created = models.DateTimeField()

    user = models.ForeignKey(get_user_model(), null=True, blank=True)

    data = models.TextField(blank=True, null=False, default="")

    valid = models.BooleanField(default=False)
    error = models.TextField(blank=True, null=True)

    def _newversion(self):
        """ Creates the new version of the page with given id. Returns the newly created version number. """
        version_query = self.page.versions

        if version_query.count() == 0:
            version = 1
        else:
            version = version_query.aggregate(Max('version'))['version__max'] + 1

        return version

    @property
    def is_published(self):
        return self == self.page.published_version

    def validate(self):
        """ Compiles the page and sets valid and error flags depending on the result. Saves the version. """
        self.valid = False

        try:
            # ToDo: поправить тут
            request = HttpRequest()
            request.user = AnonymousUser()
            context = RequestContext(request)
            render_to_string(self.page.template, yaml.load(self.data), context_instance=context)
            self.valid = True
            self.error = ""
        except (TemplateError, YAMLError), error:
            self.error = "line %s: %s" % (str(getattr(error, 'lineno', 'unknown')), str(error))

    def save(self, *args, **kwargs):
        """
        Creates the new version, validates and saves it.
        This method has a synchronization bug: we first create a new version no,
        then in other transaction save it.
        """
        if not self.date_created:
            self.date_created = datetime.now()

        if not self.version:
            self.version = self._newversion()

        try:
            self.user_id = get_current_user().id
        except AttributeError:
            self.user_id = None

        self.validate()

        super(PageVersion, self).save()

    def delete(self, using=None):
        if self.is_published:
            self.page.unpublish()

        super(PageVersion, self).delete()

    def __unicode__(self):
        return "%s:%d" % (self.page.name, self.version)


class Navigator(models.Model):
    u""" Модель навигатора """
    name = models.CharField(verbose_name=u'Название', max_length=200)

    def __unicode__(self):
        return self.name


class NavigatorItem(models.Model):
    navigator = models.ForeignKey(Navigator, related_name='items')
    name = models.CharField(verbose_name=u'Имя', max_length=200)
    index = models.IntegerField(default=0)
    url = models.URLField(max_length=500, default='', blank=True)
    page = models.ForeignKey(Page, null=True, blank=True)

    @property
    def get_url(self):
        return self.page.full_path if self.page else self.url