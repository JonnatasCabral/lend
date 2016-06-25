# -*- coding: utf-8 -*-

import os
from client.forms import CreateContainerForm
from client.forms import EditContainerForm
from client.models import Container
from client.models import CSVFile
from client.models import UploadedCode
from client.tasks import create_and_run_container
from client.tasks import run_container
from core.utils import docker
from core.views import LoginRequiredMixin
from core.views import OwnershipRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import RedirectView
from core.constants import dockerfile
from core.utils import Docker

class ContainerMixin(object):
    model = Container
    pk_url_kwarg = 'container_pk'


class ContainersListView(LoginRequiredMixin, ListView):
    template_name = 'client/containers.html'
    model = Container

    def get_queryset(self, **kwargs):
        return super(ContainersListView, self).get_queryset(
            **kwargs).filter(created_by=self.request.user).activated()


class RunningContainerView(ContainerMixin, OwnershipRequiredMixin, DetailView):
    template_name = 'client/running.html'


class CodeEditorView(ContainerMixin, OwnershipRequiredMixin, FormView):
    template_name = 'client/editor.html'
    form_class = EditContainerForm

    def get_context_data(self, **kwargs):
        context = super(CodeEditorView, self).get_context_data(**kwargs)
        context['object'] = self.object
        return context

    # def get(self, request, *args, **kwargs):
    #     container = self.get_object()
    #     is_running = docker.cli.inspect_container(
    #         container.get_object())['State']['Running']
    #     if is_running:
    #         return HttpResponseRedirect(reverse(
    #             'client:running_container', args=[container.pk]))
    #     return super(CodeEditorView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(CodeEditorView, self).get_initial()
        container = self.get_object()
        try:
            initial['csv_file'] = container.csvfile_set.latest(
                'pk').content.file
        except CSVFile.DoesNotExist:
            pass
        code = container.uploadedcode_set.latest('pk')
        initial.update({
            'title': container.title,
            'description': container.description,
            'code': code.content,
            'requirements': code.requirements
        })
        return initial

    def run_code_in_container(self, container_django):

        docker = Docker(dockerfile)
        docker_container = docker.container
        container_up = docker.container_up(docker_container, dir=container_django.pk)
        # if not docker.cli.containers():
        #     container_up = docker.container_up(docker_container, dir=container_django.pk)
        # else:
        #     container_up = docker.cli.containers()[0]["Id"]
        command='python {0}.py'.format(container_django.title)
        result = docker.container_run_command(container_up, command=command)
        return result

    def set_file(self, container, code):

        if not os.path.exists('/tmp/{0}'.format(container.pk)):
            os.makedirs('/tmp/{0}'.format(container.pk))
        file = open('/tmp/{0}/{1}.py'.format(
            container.pk,
            container.title), 'w')
        file.write(code)
        file.close()

    def form_valid(self, form):
        form_valid = super(CodeEditorView, self).form_valid(form)
        container = self.get_object()
        container.title = form.cleaned_data['title']
        container.description = form.cleaned_data.get('description')
        container.save()

        code = UploadedCode.objects.filter(container=container).latest('pk')
        if form.cleaned_data.get('code', '').strip() != code.content.strip():
            uploaded_code = UploadedCode.objects.create(
                created_by=self.request.user,
                requirements=form.cleaned_data.get('requirements'),
                container=container,
                content=form.cleaned_data.get('code')
            )
        if form.cleaned_data.get('csv_file'):
            file_obj = form.cleaned_data.get('csv_file')
            csv_files = CSVFile.objects.filter(
                    container=container)
            if csv_files.exists() and csv_files.latest(
                    'pk').content.file.name != file_obj.name or (
                        not csv_files.exists()):
                CSVFile.objects.create(
                    content=form.cleaned_data['csv_file'],
                    created_by=self.request.user,
                    container=container
                )
        self.set_file(container, form.cleaned_data.get('code'))
        container.result = self.run_code_in_container(container)
        container.save()
        return form_valid

    def get_success_url(self):
        return reverse('client:editor', args=[self.get_object().pk])


class CreateContainerView(LoginRequiredMixin, FormView):
    template_name = 'client/new.html'
    model = Container
    form_class = CreateContainerForm

    def get_form_kwargs(self):
        kwargs = super(CreateContainerView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

    def form_valid(self, form):
        form_valid = super(CreateContainerView, self).form_valid(form)
        container = Container.objects.create(
            title=form.cleaned_data.get('title'),
            description=form.cleaned_data.get('description'),
            created_by=self.request.user
        )
        UploadedCode.objects.create(
            created_by=self.request.user,
            requirements=form.cleaned_data.get('requirements'),
            container=container,
            content=form.cleaned_data.get('code')
        )
        if form.cleaned_data.get('csv_file'):
            CSVFile.objects.create(
                content=form.cleaned_data['csv_file'],
                created_by=self.request.user,
                container=container
            )
        # create_and_run_container(container.pk)
        return form_valid

    def get_success_url(self):
        return reverse('index')


class DeleteContainerView(
        ContainerMixin, OwnershipRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        container = self.get_object()
        container.deactivate()
        docker.container_rm(container.get_object())
        return super(DeleteContainerView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse('index')


code_editor_view = CodeEditorView.as_view()
containers_view = ContainersListView.as_view()
create_container_view = CreateContainerView.as_view()
delete_container_view = DeleteContainerView.as_view()
running_container_view = RunningContainerView.as_view()
