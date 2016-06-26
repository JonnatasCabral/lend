# -*- coding: utf-8 -*-

from client.enums import RUNNING_STEPS_CHOICES
from client.enums import RunningSteps
from client.utils import upload_to_user_folder
from core.models import LendModel
from django.conf import settings
from django.db import models
import os


class Container(LendModel):

    name = models.CharField(max_length=255, null=True, blank=True)
    cid = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    running = models.BooleanField(default=False)
    running_step = models.PositiveIntegerField(
        default=RunningSteps.IDLE,
        choices=RUNNING_STEPS_CHOICES
    )

    def step_loading_csv(self):
        self.running_step = RunningSteps.DATA
        self.save()

    def step_requirements(self):
        self.running_step = RunningSteps.REQUIREMENTS
        self.save()

    def step_running_code(self):
        self.running_step = RunningSteps.CODE
        self.save()

    def step_resting(self):
        self.running_step = RunningSteps.IDLE
        self.save()

    def step_finished(self):
        self.running_step = RunningSteps.FINISHED
        self.save()

    def get_object(self):
        return {
            'Id': self.cid,
            'Warnings': None
        }

    def get_code(self):
        return self.uploadedcode_set.latest('pk')

    def __unicode__(self):
        return '%s, created_by=%s' % (self.name or self.cid, self.created_by)

    class Meta:
        verbose_name = 'Container'
        verbose_name_plural = 'Containers'


class UploadedCode(LendModel):

    container = models.ForeignKey(Container)
    content = models.TextField()
    requirements = models.TextField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)

    def get_directory(self):
        return os.path.join(
            settings.MEDIA_ROOT,
            self.created_by.username,
            str(self.container.pk),
            str(self.pk)
        )

    def __unicode__(self):
        return '%s, container=%s' % (
            self.id, self.container.title
        )

    class Meta:
        verbose_name = 'Uploded Code'
        verbose_name_plural = 'Uploaded Codes'


class CSVFile(LendModel):

    container = models.ForeignKey(Container)
    content = models.FileField(upload_to=upload_to_user_folder)

    def __unicode__(self):
        return '%s, container=%s' % (
            self.id, self.container.title
        )

    class Meta:
        verbose_name = 'CSV File'
        verbose_name_plural = 'CSV Files'
