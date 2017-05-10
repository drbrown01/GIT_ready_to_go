from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^tasks$', views.create_task),
    url(r'^tasks/(?P<task_id>\d+)/destroy$', views.destroy_task),
    url(r'^tasks/(?P<task_id>\d+)/update$', views.update_task),
    url(r'^tasks/(?P<task_id>\d+)$', views.edit_task),
]
