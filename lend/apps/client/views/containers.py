# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic import ListView
from core.views import OwnershipRequiredMixin
from core.views import LoginRequiredMixin
from client.models import Container


class ContainersListView(LoginRequiredMixin, ListView):
    template_name = 'client/containers.html'
    model = Container


class CodeEditorView(OwnershipRequiredMixin, TemplateView):
    template_name = 'client/editor.html'
    model = Container
    pk_url_kwarg = 'container_pk'


code_editor_view = CodeEditorView.as_view()
containers_view = ContainersListView.as_view()
