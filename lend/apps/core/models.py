# -*- coding: utf-8 -*-

from django.db import models


class LendModel(models.Model):

    created_by = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __repr__(self):
        return u'%s(%s)' % (self.__class__.__name__, self.__unicode__())

    class Meta:
        abstract = True
