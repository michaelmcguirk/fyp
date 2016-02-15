from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new_batch/$', views.new_batch, name='new_batch'),
    url(r'^view_batch/(?P<pk>[0-9]+)/$', views.view_batch, name='view_batch'),
    url(r'^start_batch/$', views.start_batch, name='start_batch'),
    url(r'^stop_batch/$', views.stop_batch, name='stop_batch'),
    url(r'^$', views.index, name='index')
]