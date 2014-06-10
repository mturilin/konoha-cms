# -*- coding: utf-8 -*-
__author__ = 'gusevsergey'

from .models import NavigatorItem
from django import forms



class NavigatorItemInlineForm(forms.ModelForm):
    class Meta:
        model = NavigatorItem

    def clean(self):
        cd = super(NavigatorItemInlineForm, self).clean()
        if cd.get('url') and cd.get('page'):
            raise forms.ValidationError(u"Нужно заполнить либо поле URL либо Page.")
        return cd
