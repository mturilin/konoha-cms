# -*- coding: utf-8 -*-
__author__ = 'gusevsergey'

from .models import Navigator


def navigator(name):
    try:
        return Navigator.objects.get(name=name).items.order_by('index')
    except Navigator.DoesNotExist:
        return []