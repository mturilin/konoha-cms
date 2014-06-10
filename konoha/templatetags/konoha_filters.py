import json
from django.core.exceptions import ObjectDoesNotExist
from konoha import KonohaError
from konoha.models import Page


__author__ = 'mikhailturilin'

from coffin import template

register = template.Library()

@register.test()
def has_attribute(obj, attribute):
    return hasattr(obj, attribute)


@register.filter()
def konoha_page_url(name):
    try:
        return Page.objects.get(name=name).full_path
    except ObjectDoesNotExist:
        return KonohaError('Page %s does not exist' % name)

@register.filter()
def to_json(value):
    return json.dumps(value)
