# -*- coding: utf-8 -*-

from client.models import Container
from client.tasks import run_command_in_container
from core.utils import docker
import os


class RunMixin(object):

    def run_code_in_container(self, container_model, **options):
        docker_container = self.get_or_create_container(container_model)
        container_model.running = True
        container_model.stopped = False
        container_model.step_resting()
        run_command_in_container.delay(docker_container, **options)

    def set_code_file(self, container, code):
        media = code.get_directory()
        if not os.path.exists(media):
            os.makedirs(media)

        filepath = os.path.join(media, '{}.py'.format(container.title))
        if code.requirements:
            requirements = os.path.join(media, 'requirements.txt')
            with open(requirements, 'wb') as reqfile:
                reqfile.write(code.requirements)
        with open(filepath, 'wb') as codefile:
            codefile.write(code.content)

    def get_or_create_container(self, container):
        if not container.cid:
            container_data = docker.cli.inspect_container(
                docker.container_create())
            container.cid = container_data['Id']
            container.name = container_data['Name'].strip('/')
            container.save()
        return container.get_object()


class ContainerMixin(object):
    model = Container
    pk_url_kwarg = 'container_pk'
