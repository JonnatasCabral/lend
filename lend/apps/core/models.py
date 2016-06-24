from __future__ import unicode_literals

from django.db import models

# Create your models here.


class LendModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __repr__(self):
        return u'%s(%s)' % (self.__class__.__name__, self.__unicode__())
