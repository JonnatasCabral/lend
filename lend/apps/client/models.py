# -*- coding: utf-8 -*-

from client.utils import upload_to_user_folder
from core.models import LendModel
from django.db import models


class Container(LendModel):

    name = models.CharField(max_length=255, null=True, blank=True)
    cid = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def get_object(self):
        return {
            'Id': self.cid,
            'Warnings': None
        }

    def __unicode__(self):
        return '%s, created_by=%s' % (self.name or self.cid, self.created_by)

    class Meta:
        verbose_name = 'Container'
        verbose_name_plural = 'Containers'


class UploadedCode(LendModel):

    container = models.ForeignKey(Container)
    content = models.TextField()
    requirements = models.TextField(null=True, blank=True)

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
