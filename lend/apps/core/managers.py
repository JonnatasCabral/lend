# -*- coding: utf-8 -*-

from django.db import models


class LendQuerySet(models.QuerySet):

    def activated(self):
        return self.filter(active=True)

    def deactivated(self):
        return self.filter(active=False)
