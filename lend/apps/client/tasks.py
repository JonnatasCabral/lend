# -*- coding: utf-8 -*-

from client.models import Container
from core.utils import docker


def create_and_run_container(container_id, command):
    container = Container.objects.get(pk=container_id)
    if not container.cid:
        container_data = docker.cli.inspect_container(
            docker.container_create())
        container.cid = container_data['Id']
        container.name = container_data['Name']
        container.save()

    docker.container_run_command(container.get_object(), command)


def run_container(container_id, command):
    container = Container.objects.get(pk=container_id)
    if container.cid:
        docker.container_run_command(container.get_object(), command)
