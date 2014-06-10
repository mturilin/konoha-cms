# coding=utf-8
from functools import wraps
from .django_ace import AceWidget
from .models import Page, Navigator, NavigatorItem
from .forms import NavigatorItemInlineForm
from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.shortcuts import *
from funcy import walk
from treeadmin.admin import TreeAdmin



__author__ = 'mturilin'


def get_template_choices():
    return [('', '')] + sorted(((template, name) for (name, template) in settings.KONOHA_TEMPLATES.iteritems()),
                               key=lambda pair: pair[1])


class PageAdminForm(forms.ModelForm):
    """
    Form for Konoha  page admin
    """
    template = forms.ChoiceField(choices=get_template_choices())

    def __init__(self, *args, **kwargs):
        """
        I need to redefine this method to update template choices if settings.KONOHA_TEMPLATES were changes from initial
        value after the import. For now this is needed for unit tests, when we redefine KONOHA_TEMPLATES from the
        production to the test predefined values.
        """
        super(PageAdminForm, self).__init__(*args, **kwargs)

        self.fields['template'] = forms.ChoiceField(choices=get_template_choices())

    class Meta:
        model = Page

        widgets = {
            'data': AceWidget(mode='yaml', theme='solarized_light', width="100%", height="400px"),
        }


def staff_only_view_method(view_method):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """

    @wraps(view_method)
    def _checklogin(*args, **kwargs):
        request = None
        try:
            request = kwargs['request']
        except KeyError:
            for arg in args:
                if isinstance(arg, HttpRequest):
                    request = arg
                    break
            if not request:
                raise ValueError('request is not provided in the view method')

        if request.user.is_active and request.user.is_staff:
            # The user is valid. Continue to the admin page.
            return view_method(*args, **kwargs)

        return redirect("admin:index")

    return _checklogin


class PageAdmin(TreeAdmin):
    """ This is the main admin class """
    form = PageAdminForm

    mptt_level_indent = 20

    list_display = ['indented_short_title', 'template_name', 'path_link', 'published_tag', 'num_versions']
    list_display_links = ['indented_short_title']

    #list_filter = ('published',)

    #actions = ['make_published', 'make_unpublished']

    readonly_fields = ('published_tag', 'published_version')

    def indented_short_title(self, obj):
        return super(PageAdmin, self).indented_short_title(obj)

    indented_short_title.short_description = 'Name'
    indented_short_title.allow_tags = True

    def num_versions(self, obj):
        return obj.versions.count()

    num_versions.short_description = 'Versions'

    def path_link(self, obj):
        return "<a href='%s'>%s</a>" % (obj.full_path, obj.path)

    path_link.allow_tags = True
    path_link.short_description = "Path"

    def published_tag(self, obj):
        if obj.published:
            return "True <a class='button' href='%sunpublish/'>Unpublish</a>" % reverse('admin:konoha_page_change',
                                                                                        args=[obj.pk])
        else:
            return "False <a class='button' href='%spublish_version/%d/'>Publish</a>" % \
                   (reverse('admin:konoha_page_change', args=[obj.pk]), obj.latest_version.version)

    published_tag.allow_tags = True
    published_tag.short_description = "Published"

    def template_name(self, obj):
        try:
            return walk(reversed, settings.KONOHA_TEMPLATES)[obj.template]
        except KeyError:
            return obj.template

    template_name.short_description = "Template"

    def get_urls(self):
        urls = super(PageAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'(?P<page_id>\d+)/publish_version/(?P<version_id>\d+)/$',
                self.admin_site.admin_view(self.publish_view),
                name='konoha_page_publish_version'),

            url(r'(?P<page_id>\d+)/validate_version/(?P<version_id>\d+)/$',
                self.admin_site.admin_view(self.validate_view),
                name='konoha_page_validate_version'),

            url(r'(?P<page_id>\d+)/delete_version/(?P<version_id>\d+)/$',
                self.admin_site.admin_view(self.delete_version_view),
                name='konoha_page_delete_version'),

            url(r'(?P<page_id>\d+)/unpublish/$', self.admin_site.admin_view(self.unpublish_view),
                name='konoha_page_unpublish'),
        )
        return my_urls + urls

    @staff_only_view_method
    def publish_view(self, request, page_id, version_id):
        page = get_object_or_404(Page, id=int(page_id))
        version = page.versions.get(version=int(version_id))

        page.publish(version)

        return redirect(reverse("admin:konoha_page_change", args=[page_id]))

    @staff_only_view_method
    def unpublish_view(self, request, page_id):
        page = get_object_or_404(Page, id=int(page_id))

        page.unpublish()

        return redirect(reverse("admin:konoha_page_change", args=[page_id]))

    @staff_only_view_method
    def validate_view(self, request, page_id, version_id):
        page = get_object_or_404(Page, id=int(page_id))
        version = page.versions.get(version=int(version_id))

        #version.validate()
        version.save()

        return redirect(reverse("admin:konoha_page_change", args=[page_id]))

    @staff_only_view_method
    def delete_version_view(self, request, page_id, version_id):
        page = get_object_or_404(Page, id=int(page_id))
        version = page.versions.get(version=int(version_id))

        #version.validate()
        if version != page.latest_version:
            version.delete()

        return redirect(reverse("admin:konoha_page_change", args=[page_id]))

admin.site.register(Page, PageAdmin)


class NavigatorItemInline(admin.TabularInline):
    model = NavigatorItem
    extra = 0
    form = NavigatorItemInlineForm


class NavigatorAdmin(admin.ModelAdmin):
    inlines = [NavigatorItemInline]

admin.site.register(Navigator, NavigatorAdmin)