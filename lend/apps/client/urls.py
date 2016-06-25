# -*- coding: utf-8 -*-

from client.views import code_editor_view
from client.views import containers_view
from django.conf.urls import url

urlpatterns = [
    url(r'^containers/$', containers_view, name='containers'),
    url(r'^containers/(?P<container_pk>[\d]+)/$',
        code_editor_view, name='editor')
]
