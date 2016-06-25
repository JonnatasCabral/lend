# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class OwnershipRequiredMixin(object):
    model = None
    pk_url_kwarg = 'pk'

    def get_object(self):
        self.object = get_object_or_404(
            self.model.objects.filter(created_by=self.request.user),
            pk=self.kwargs[self.pk_url_kwarg]
        )
        return self.object

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.get_object()
        return super(OwnershipRequiredMixin, self).dispatch(
            request, *args, **kwargs)
