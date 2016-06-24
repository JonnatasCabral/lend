# -*- coding: utf-8 -*-

from core.models import LendModel
from django.db import models


class Container(LendModel):

    created_by = models.ForeignKey('socialaccount.SocialAccount')
    name = models.CharField(max_length=255, null=True, blank=True)
    cid = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return '%s, created_by=%s' % (self.name or self.cid, self.created_by)
