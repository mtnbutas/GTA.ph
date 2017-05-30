from django.conf.urls import url
from django.views.generic.edit import CreateView

from views import ckeditor_form_view, post_edit
from views import post_detail
from . import forms

urlpatterns = [
    url(r'^create/$', ckeditor_form_view, name='post-create'),
    url(r'^edit/(?P<post_id>\d+)/$', post_edit, name='post-edit'),
    url(r'^(?P<post_id>\d+)/$', post_detail, name='post-detail'),
    url(r'^(?P<post_id>\d+)/(?P<slug>[-\w\d]+)/$', post_detail, name='post-detail'),
]