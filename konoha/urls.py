from .views import page
from django.conf.urls import url, patterns


__author__ = 'mturilin'

urlpatterns = patterns(
    '',
    # url(r'^files/(?P<path>[0-9A-Za-z-_.//]+)$','django.views.static.serve', {
    #     'document_root': settings.KONOHA_FILES_ROOT,
    #     }),
    url(r'^(?P<path>[0-9A-Za-z-_.//]+)$', page, name='page-by-path'),
    )