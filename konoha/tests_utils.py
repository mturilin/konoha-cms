# -*- coding: utf-8 -*-
__author__ = 'gusevsergey'

from django.template.response import TemplateResponse

from django.test.simple import DjangoTestSuiteRunner
from jinja2 import Template as Jinja2Template
from django.test import signals


def konoha_instrumented_render(template, *args, **kwargs):
    context = dict(*args, **kwargs)
    if not template.filename == '<template>':
        signals.template_rendered.send(sender=template, template=template, context=context)
    return Jinja2Template.original_render(template, *args, **kwargs)


class KonohaTestSuiteRunner(DjangoTestSuiteRunner):
    def setup_test_environment(self, **kwargs):
        super(KonohaTestSuiteRunner, self).setup_test_environment(**kwargs)

        Jinja2Template.original_render = Jinja2Template.render
        Jinja2Template.render = konoha_instrumented_render

    def teardown_test_environment(self, **kwargs):
        super(KonohaTestSuiteRunner, self).teardown_test_environment(**kwargs)

        Jinja2Template.render = Jinja2Template.original_render
        del Jinja2Template.original_render
