# -*- coding: utf-8 -*-

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'core/index.html'


class LoginView(TemplateView):
    template_name = 'core/login.html'


index_view = IndexView.as_view()
login_view = LoginView.as_view()
