# -*- coding: utf-8 -*-

from client.views import code_editor_view
from client.views import containers_view
from client.views import create_container_view
from client.views import delete_container_view
from client.views import stop_container_view
from django.conf.urls import url

urlpatterns = [
    url(r'^containers/$', containers_view, name='containers'),
    url(r'^containers/new/$', create_container_view, name='create_container'),
    url(r'^containers/(?P<container_pk>[\d]+)/$',
        code_editor_view, name='editor'),
    url(r'^containers/delete/(?P<container_pk>[\d]+)/$',
        delete_container_view, name='delete_container'),
    url(r'^containers/stop/(?P<container_pk>[\d]+)/$',
        stop_container_view, name='stop_container')
]
