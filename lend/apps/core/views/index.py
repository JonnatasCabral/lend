# -*- coding: utf-8 -*-

from django.views.generic import RedirectView
from django.views.generic import TemplateView
from core.views.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse


class IndexRedirectView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self):
        return reverse('index')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'


index_view = IndexView.as_view()
index_redirect_view = IndexRedirectView.as_view()
