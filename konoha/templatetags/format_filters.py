# coding=utf-8
__author__ = 'mikhailturilin'
import datetime
from django.utils.formats import get_format
from django.utils import numberformat, translation
from coffin import template

register = template.Library()


@register.filter()
def decimal(value, decimal_pos=None, thousand_separator=None):
    if not value: return ''

    if thousand_separator:
        grouping = 3
        thousand_sep = thousand_separator
        force_grouping = True
    else:
        grouping = 0
        thousand_sep = ''
        force_grouping = False

    lang = translation.get_language()
    decimal_sep = get_format('DECIMAL_SEPARATOR', lang, use_l10n=True)

    return numberformat.format(value, decimal_sep, decimal_pos, grouping, thousand_sep, force_grouping)

#
#@register.filter()
#def date(value, date_format='medium'):
#    if not value: return ''
#
#    if date_format == 'full':
#        date_format = "EEEE, d. MMMM y"
#    elif date_format == 'medium':
#        date_format = "dd.MM.y"
#
#    return format_date(value, date_format, locale='ru')
#
#@register.filter()
#def time(value, time_format='medium'):
#    if not value: return ''
#
#    return format_time(value, time_format, locale='ru')


@register.filter()
def strftime(value, format_string):
    return value.strftime(format_string)


@register.filter()
def pager(seq, offset, number_of_elements):
    if len(seq) < offset:
        return []

    if len(seq) > offset + number_of_elements:
        return seq[offset: offset + number_of_elements]

    return seq[offset:]


@register.filter()
def unix_time(time_value):
    if not time_value: return ''

    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = time_value - epoch
    return int(delta.total_seconds())


@register.filter()
def floatdot(value, decimal_pos=2):
    if not value:
        return 0

    return numberformat.format(value, ".", decimal_pos)

