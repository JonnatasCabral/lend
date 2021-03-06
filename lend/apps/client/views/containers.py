# -*- coding: utf-8 -*-

from client.enums import RUNNING_STEPS_CHOICES
from client.forms import CreateContainerForm
from client.forms import EditContainerForm
from client.forms import StopContainerForm
from client.models import Container
from client.models import CSVFile
from client.models import UploadedCode
from client.tasks import stop_and_remove_container
from client.tasks import stop_container
from client.views.mixins import ContainerMixin
from client.views.mixins import RunMixin
from core.constants import editor_initial_comment
from core.views import LoginRequiredMixin
from core.views import OwnershipRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import View


class ContainersListView(LoginRequiredMixin, ListView):
    template_name = 'client/containers.html'
    model = Container

    def get_queryset(self, **kwargs):
        return super(ContainersListView, self).get_queryset(
            **kwargs).filter(created_by=self.request.user).activated()


class StopContainerView(ContainerMixin, OwnershipRequiredMixin, View):
    form_class = StopContainerForm

    def post(self, request, *args, **kwargs):
        container = self.get_object()
        stop_container.delay(container.get_object())
        return HttpResponseRedirect(
            reverse('client:editor', args=[self.get_object().pk])
        )


class CodeEditorView(
        RunMixin, ContainerMixin, OwnershipRequiredMixin, FormView):
    template_name = 'client/editor.html'
    form_class = EditContainerForm

    def get_form_kwargs(self):
        kwargs = super(CodeEditorView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'instance': self.get_object()
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CodeEditorView, self).get_context_data(**kwargs)
        context.update({
            'object': self.get_object(),
            'result': self.get_object().get_code().result,
            'actual_step': dict(RUNNING_STEPS_CHOICES)[
                self.get_object().running_step],
            'initial_comment': editor_initial_comment
        })
        return context

    def get_initial(self):
        initial = super(CodeEditorView, self).get_initial()
        container = self.get_object()
        data_file = container.get_csv_file()
        if data_file:
            initial['csv_file'] = data_file.content.file
        code = container.get_code()
        initial.update({
            'title': container.title,
            'description': container.description,
            'code': code.content,
            'requirements': code.requirements
        })
        return initial

    def form_valid(self, form):
        form_valid = super(CodeEditorView, self).form_valid(form)
        container = self.get_object()
        container.title = form.cleaned_data['title']
        container.description = form.cleaned_data.get('description')
        container.save()
        keep_requirements = form.cleaned_data.get('keep_requirements', False)
        init_code = UploadedCode.objects.filter(
            container=container).latest('pk')
        if form.cleaned_data.get(
                'code', '').strip() != init_code.content.strip():
            code = UploadedCode.objects.create(
                created_by=self.request.user,
                requirements=form.cleaned_data.get('requirements'),
                container=container,
                content=form.cleaned_data.get('code')
            )
        else:
            code = init_code
            code.requirements = form.cleaned_data.get('requirements')
            code.save()

        if form.cleaned_data.get('csv_file'):
            file_obj = form.cleaned_data.get('csv_file')
            csv_files = CSVFile.objects.filter(container=container)

            if csv_files.exists() and csv_files.latest(
                    'pk').content.file.name != file_obj.name or (
                        not csv_files.exists()):
                CSVFile.objects.create(
                    content=form.cleaned_data['csv_file'],
                    created_by=self.request.user,
                    container=container
                )

        self.set_code_file(container, code)
        self.run_code_in_container(
            container,
            keep_requirements=keep_requirements
        )
        return form_valid

    def get_success_url(self):
        return reverse('client:editor', args=[self.get_object().pk])


class CreateContainerView(RunMixin, LoginRequiredMixin, FormView):
    template_name = 'client/new.html'
    model = Container
    form_class = CreateContainerForm

    def get_form_kwargs(self):
        kwargs = super(CreateContainerView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateContainerView, self).get_context_data(**kwargs)
        context.update({
            'initial_comment': editor_initial_comment
        })
        return context

    def form_valid(self, form):
        self.container = Container.objects.create(
            title=form.cleaned_data.get('title'),
            description=form.cleaned_data.get('description'),
            created_by=self.request.user
        )
        code = UploadedCode.objects.create(
            created_by=self.request.user,
            requirements=form.cleaned_data.get('requirements'),
            container=self.container,
            content=form.cleaned_data.get('code')
        )
        if form.cleaned_data.get('csv_file'):
            CSVFile.objects.create(
                content=form.cleaned_data['csv_file'],
                created_by=self.request.user,
                container=self.container
            )
        self.set_code_file(self.container, code)
        self.run_code_in_container(self.container)
        return super(CreateContainerView, self).form_valid(form)

    def get_success_url(self):
        return reverse('client:editor', args=[self.container.id])


class DeleteContainerView(
        ContainerMixin, OwnershipRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        container = self.get_object()
        container.deactivate()
        stop_and_remove_container.delay(container.get_object())
        return super(DeleteContainerView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse('index')


code_editor_view = CodeEditorView.as_view()
containers_view = ContainersListView.as_view()
create_container_view = CreateContainerView.as_view()
delete_container_view = DeleteContainerView.as_view()
stop_container_view = StopContainerView.as_view()
