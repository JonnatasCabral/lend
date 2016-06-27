# -*- coding: utf-8 -*-

from client.models import Container
from core.constants import csv_parser
from core.utils import docker
import celery
import functools
import os


@celery.task
def run_command_in_container(container, **options):
    container_model = Container.objects.get(cid=container['Id'])
    code = container_model.get_code()
    csv_file = container_model.get_csv_file()

    container_up = docker.container_up(
        container, directory=code.get_directory())
    command = 'python {}.py'.format(container_model.title)
    run = functools.partial(docker.container_run_command, container_up)

    if csv_file:
        container_model.step_loading_csv()
        csv_python_file = csv_parser.format(
            datafile=os.path.basename(csv_file.content.file.name),
        )
        csv_path = os.path.join(code.get_directory(), 'lendcsv.py')
        with open(csv_path, 'wb') as f:
            f.write(csv_python_file)

    pip_install = 'pip install -r requirements.txt'
    container_model.step_requirements()
    if not options.get('keep_requirements', False):
        pip_uninstall = (
            '/bin/sh -c "pip freeze > uninstall.txt" &&'
            ' pip uninstall -r uninstall.txt -y && rm uninstall.txt'
        )
        run(command=pip_uninstall)
    if code.requirements:
        run(command=pip_install)

    container_model.step_running_code()
    code.result = run(command=command)
    code.save()

    container_model.step_finished()
    stop_container.delay(container)
    container_model.running = False
    container_model.save()


@celery.task
def stop_and_remove_container(container):
    container_model = Container.objects.filter(
        cid=container['Id']).latest('pk')
    if container_model.cid:
        docker.container_rm(container)
    container_model.cid = None
    container_model.name = None
    container_model.save()


@celery.task
def stop_container(container):
    container_model = Container.objects.filter(
        cid=container['Id']).latest('pk')
    if container_model.cid:
        docker.container_down(container)
    container_model.stopped = True
    container_model.save()
