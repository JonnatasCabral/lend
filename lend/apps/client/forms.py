# -*- coding: utf-8 -*-

from django import forms
from core.fields import BSCharField
from core.fields import BSTextField
from client.models import Container
import re


class CreateContainerForm(forms.Form):

    title = BSCharField(required=True, placeholder='Name your Container')
    description = BSCharField(required=False, placeholder='Description')
    code = BSTextField(required=True)
    csv_file = forms.FileField(required=False)
    requirements = BSTextField(
        required=False,
        placeholder=(
            'Paste your PyPI requirements here.\n'
            'Examples:\nnumpy==1.11.0\npandas==0.18.1'
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateContainerForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')

        clean_code = code.strip().split('\n')
        for i, line in enumerate(clean_code):
            clean_code[i] = re.sub('^(\s?)\#.+', '', line) or None
        clean_code = filter(lambda x: x is not None, clean_code)
        if not clean_code:
            self.add_error('code', 'This field is required.')
        return code

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip().lower()
        if not title:
            self.add_error('title', 'This field is required.')

        if len(title) > 25:
            self.add_error('title', 'Character limit is 25.')
        if Container.objects.activated().filter(
                created_by=self.user, title=title.strip().lower()).exists():
            self.add_error('title', 'This name is taken.')
        return title

    def clean(self):
        cleaned_data = super(CreateContainerForm, self).clean()
        data = cleaned_data.copy()
        for field, value in cleaned_data.iteritems():
            if not value:
                data.pop(field)
        return data


class EditContainerForm(CreateContainerForm):
    pass
