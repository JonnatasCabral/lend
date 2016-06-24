# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout


class IndexView(TemplateView):
    template_name = 'core/index.html'


class LoginView(TemplateView):
    template_name = 'core/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super(LoginView, self).dispatch(request, *args, **kwargs)


class LogoutView(RedirectView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse('index')


index_view = IndexView.as_view()
login_view = LoginView.as_view()
logout_view = LogoutView.as_view()
