# -*- coding: utf-8 -*-

from client.models import Container
from core.utils import docker
import celery


@celery.task
def run_command_in_container(container):
    container_model = Container.objects.get(cid=container['Id'])
    code = container_model.get_code()
    container_up = docker.container_up(
        container, directory=code.get_directory())
    command = 'python {}.py'.format(container_model.title)
    pip_install = 'pip install -r requirements.txt'

    container_model.step_loading_csv()
    # TODO load CSV data

    container_model.step_requirements()
    docker.container_run_command(container_up, command=pip_install)

    container_model.step_running_code()
    code.result = docker.container_run_command(container_up, command=command)
    code.save()

    container_model.step_finished()
    stop_container.delay(container)
    container_model.running = False
    container_model.save()


@celery.task
def stop_and_remove_container(container):
    container_model = Container.objects.get(cid=container['Id'])
    if container_model.cid:
        docker.container_rm(container)
    container_model.cid = None
    container_model.name = None
    container_model.save()


@celery.task
def stop_container(container):
    container_model = Container.objects.get(cid=container['Id'])
    if container_model.cid:
        docker.container_down(container)
    container_model.running = False
    container_model.save()
