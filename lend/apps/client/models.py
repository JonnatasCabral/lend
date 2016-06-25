# -*- coding: utf-8 -*-

from core.models import LendModel
from django.db import models


class Container(LendModel):

    name = models.CharField(max_length=255, null=True, blank=True)
    cid = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return '%s, created_by=%s' % (self.name or self.cid, self.created_by)

    class Meta:
        verbose_name = 'Container'
        verbose_name_plural = 'Containers'


class UploadedCode(LendModel):

    container = models.ForeignKey(Container)
    content = models.TextField()
    requirements = models.TextField()

    def __unicode__(self):
        return '%s, container=%s' % (
            self.id, self.container.name or self.container.cid
        )

    class Meta:
        verbose_name = 'Uploded Code'
        verbose_name_plural = 'Uploaded Codes'


class CSVFile(LendModel):

    content = models.TextField()

    def __unicode__(self):
        return '%s, container=%s' % (
            self.id, self.container.name or self.container.cid
        )

    class Meta:
        verbose_name = 'CSV File'
        verbose_name_plural = 'CSV Files'


class CSVFileCode(LendModel):
    csv_file = models.ForeignKey(CSVFile)
    uploaded_code = models.ForeignKey(UploadedCode)

    def __unicode__(self):
        return 'csv=%s, code=%s' % (self.csv_file.id, self.uploaded_code.id)
