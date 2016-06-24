# -*- coding: utf-8 -*-

from allauth.socialaccount.providers.github.views import oauth2_callback
from allauth.socialaccount.providers.github.views import oauth2_login
from core.views import index_redirect_view
from core.views import index_view
from django.conf.urls import include
from django.conf.urls import url


accounts_patterns = [
    url(r'^login/$', oauth2_login, name='github_login'),
    url(r'^login/callback/$', oauth2_callback, name='github_callback'),
    url(r'^profile/$', index_redirect_view)
]

urlpatterns = [
    url(r'^accounts/', include(accounts_patterns)),
    url('', index_view, name='index')
]
