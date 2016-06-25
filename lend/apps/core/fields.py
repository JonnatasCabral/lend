# -*- coding: utf-8 -*-

from django.forms import CharField
from django.forms import TextInput
from django.forms import Textarea


class TextFormControlWidgetMixin(object):

    def render(self, name, value, attrs=None):
        attrs.update({
            'class': 'form-control',
        })
        return super(TextFormControlWidgetMixin, self).render(
            name, value, attrs)


class FormControlFieldMixin(object):

    def __init__(self, *args, **kwargs):
        placeholder = kwargs.pop('placeholder', None)
        super(FormControlFieldMixin, self).__init__(*args, **kwargs)
        if placeholder:
            self.widget.attrs.update({'placeholder': placeholder})


class CharFieldFormControl(TextFormControlWidgetMixin, TextInput):
    pass


class TextFieldFormControl(TextFormControlWidgetMixin, Textarea):
    pass


class BSCharField(FormControlFieldMixin, CharField):
    widget = CharFieldFormControl


class BSTextField(FormControlFieldMixin, CharField):
    widget = TextFieldFormControl
