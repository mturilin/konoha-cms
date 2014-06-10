from django.conf import settings
from django.conf.urls import patterns
from django.test import Client
from lettuce import step, before, world
from konoha.models import Page
from path import path
__author__ = 'mikhailturilin'

urlpatterns = patterns(
    '....views',
    (r'^(?P<path>[0-9A-Za-z-_.//]*)$', 'page'),
)


@before.all
def set_django_client():
    world.client = Client()

@before.all
def set_konoha_test_urls():
    settings.ROOT_URLCONF = __name__

@before.all
def set_konoha_test_templates():
    settings.TEMPLATE_DIRS = (
        path(__file__).dirname().dirname().joinpath('templates')
    )
#
#@before.all
#def set_konoha_app():
#    settings.INSTALLED_APPS = ['konoha']

@step("Page '(\w+)' with url '(.*)' and template '(.*)'")
def define_page(step, name, url, template):
    print "Define page %s" % name
    Page.objects.create(name=name, data="", template=template, path=url.lstrip('/'))



@step("We request url '(.*)' from server")
def get_url(step, url):
    world.response = world.client.get(url)

@step("Returned page contains '(.*)'")
def returned_page_contains(step, text):
    assert text in world.response.content