# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from core.views import OwnershipRequiredMixin
from client.models import Container


class CodeEditorView(OwnershipRequiredMixin, TemplateView):
    template_name = 'client/editor.html'
    model = Container
    pk_url_kwarg = 'container_pk'


code_editor_view = CodeEditorView.as_view()
