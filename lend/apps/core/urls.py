# -*- coding: utf-8 -*-

from allauth.account.views import logout
from allauth.socialaccount.providers.github.views import oauth2_callback
from allauth.socialaccount.providers.github.views import oauth2_login
from core.views import index_view
from core.views import login_view
from django.conf.urls import include
from django.conf.urls import url

accounts_patterns = [
    url(r'^login/$', oauth2_login, name='github_login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/callback/$', oauth2_callback, name='github_callback'),
]

urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^accounts/', include(accounts_patterns)),
    url(r'^login/', login_view, name='login'),
]
