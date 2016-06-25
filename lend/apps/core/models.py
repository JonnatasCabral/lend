# -*- coding: utf-8 -*-

from django.db import models
from core.managers import LendQuerySet


class LendModel(models.Model):

    created_by = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    objects = LendQuerySet.as_manager()

    def __logical_state(self, state):
        self.active = state
        self.save(update_fields=['active'])
        return self

    def deactivate(self):
        return self.__logical_state(False)

    def activate(self):
        return self.__logical_state(True)

    def __repr__(self):
        return u'%s(%s)' % (self.__class__.__name__, self.__unicode__())

    class Meta:
        abstract = True
