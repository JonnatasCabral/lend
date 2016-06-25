# -*- coding: utf-8 -*-

from client.forms import CreateContainerForm
from client.models import Container
from core.views import LoginRequiredMixin
from core.views import OwnershipRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import TemplateView


class ContainerMixin(object):
    model = Container
    pk_url_kwarg = 'container_pk'


class ContainersListView(LoginRequiredMixin, ListView):
    template_name = 'client/containers.html'
    model = Container

    def get_queryset(self, **kwargs):
        return super(ContainersListView, self).get_queryset(
            **kwargs).activated()


class CodeEditorView(ContainerMixin, OwnershipRequiredMixin, TemplateView):
    template_name = 'client/editor.html'


class CreateContainerView(LoginRequiredMixin, FormView):
    template_name = 'client/new.html'
    model = Container
    form_class = CreateContainerForm


class DeleteContainerView(
        ContainerMixin, OwnershipRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        container = self.get_object()
        container.deactivate()
        return super(DeleteContainerView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse('index')


code_editor_view = CodeEditorView.as_view()
containers_view = ContainersListView.as_view()
create_container_view = CreateContainerView.as_view()
delete_container_view = DeleteContainerView.as_view()
