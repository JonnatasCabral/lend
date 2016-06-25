# -*- coding: utf-8 -*-

from django import forms
from core.fields import BSCharField
from core.fields import BSTextField


class CreateContainerForm(forms.Form):

    title = BSCharField(placeholder='Name your Container')
    description = BSCharField(placeholder='Description')
    requirements = BSTextField(
        placeholder=(
            'Paste your PyPI requirements here.\n'
            'Examples:\nnumpy==1.11.0\npandas==0.18.1'
        )
    )
