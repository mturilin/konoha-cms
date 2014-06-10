from coffin.shortcuts import render

__author__ = 'mikhailturilin'
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()


def filter_tests2(request):
    class TestObject(object):
        testattribute = "bloblo"

    testobject = TestObject()
    return render(request, "tests/filters.html", {'testobject': testobject})


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^filter_tests2$', filter_tests2),
    url(r'^(?P<path>[0-9A-Za-z-_.//]*)$', 'konoha.views.page', name="page-by-path"),
)
