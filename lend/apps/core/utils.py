# -*- coding: utf-8 -*-

from client.models import Container
from core.constants import dockerfile
from django.conf import settings
from docker import Client
from docker.errors import NotFound
from io import BytesIO
import os


class Docker(object):

    cli = None
    image = None
    container = None

    def __init__(self, dockerfile):
        self.cli = Client(base_url='unix://var/run/docker.sock')
        self.image = self.create_image(dockerfile)

    def create_image(self, dockerfile, tag='python/lend', rm=True):
        f = BytesIO(dockerfile)

        response = [line for line in self.cli.build(
            fileobj=f, rm=rm, tag=tag
        )]
        return response

    def container_create(self):
        container = self.cli.create_container(
            image='python/lend',
            stdin_open=True,
            volumes={"/tmp/": {}},
            tty=True,
            command='/bin/sh',
        )
        return container

    def container_up(self, container, directory=''):
        """
        Recebe um dict com Id do container e roda o container
        """
        directory = os.path.join(settings.MEDIA_ROOT, directory)

        try:
            self.cli.inspect_container(container)
        except NotFound:
            container_model = Container.objects.get(cid=container['Id'])
            container = self.container_create()
            data = docker.cli.inspect_container(container)
            container_model.cid = data['Id']
            container_model.name = data['Name']
            container_model.save()
        self.cli.start(container,  binds=["{}:/home/codes".format(directory)])
        return self.cli.containers()[0]["Id"]

    def container_down(self, container):
        try:
            return self.cli.stop(container)
        except NotFound:
            return

    def container_rm(self, container):
        try:
            self.container_down(container)
            return self.cli.remove_container(container)
        except NotFound:
            return

    def container_run_command(self, container, command):
        """
        Recebe um container e um comando, o ultimo no formato de str. Retorna
        o um dict com a chave para essa execução.
        """
        r = self.cli.exec_create(container, command)
        return self.container_response(r)

    def container_response(self, exec_create):
        """
        Recebe um dict com a chave da execução de um exec_create
        e retorna o resultado que o bash retornou.
        """
        return self.cli.exec_start(exec_create)


docker = Docker(dockerfile)
