from django.conf.urls import url
from client.views import index
from client.views import code_editor

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^code-editor/$', code_editor, name="code_editor"),
]
