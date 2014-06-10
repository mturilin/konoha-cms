from django.conf import settings
from import_helpers import build_funcmodule_map
from konoha.templatetags.konoha_filters import konoha_page_url

__author__ = 'mikhailturilin'


def datasources(request):
    return {
        'DATASOURCES': build_funcmodule_map(settings.KONOHA_DATASOURCES)
    }


def page_url(request):
    return {
        'KONOHA_PAGE_URL': konoha_page_url
    }
