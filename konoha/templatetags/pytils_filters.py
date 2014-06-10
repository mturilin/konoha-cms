# -*- coding:utf-8 -*-
__author__ = 'gusevsergey'
from pytils import dt
from coffin import template

register = template.Library()


@register.filter()
def date_inflected(d, date_format):
    return dt.ru_strftime(unicode(date_format), d, inflected=True)

