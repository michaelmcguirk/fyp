from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new_batch/$', views.new_batch, name='new_batch'),
    url(r'^$', views.index, name='index')
]