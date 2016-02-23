from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new_batch/$', views.new_batch, name='new_batch'),
    url(r'^edit_batch/(?P<pk>[0-9]+)/$', views.edit_batch, name='edit_batch'),
    url(r'^view_batch/(?P<pk>[0-9]+)/$', views.view_batch, name='view_batch'),
    url(r'^compare/(?P<pk>[0-9]+)/$', views.compare, name='compare'),
    url(r'^start_batch/$', views.start_batch, name='start_batch'),
    url(r'^stop_batch/$', views.stop_batch, name='stop_batch'),
    url(r'^serve_compare_chart/(?P<b1>[0-9]+)/(?P<b2>[0-9]+)/$', views.serve_compare_chart, name='serve_compare_chart'),
    url(r'^view_user_batches/(?P<pk>[0-9]+)/$', views.view_user_batches, name='view_user_batches'),
    url(r'^register/$', views.register, name='register'),
    url(r'^$', views.index, name='index')
]