# -*- coding: utf-8 -*-

from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import multiprocessing
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lend.settings')
app = Celery('lend')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERYD_CONCURRENCY=(multiprocessing.cpu_count() * 2) + 1,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ENABLE_UTC=True,
    CELERY_TIMEZONE='America/Recife',
    BROKER_POOL_LIMIT=1
)
