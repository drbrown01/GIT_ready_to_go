from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.signin),
	url(r'^users/login$', views.login),
	url(r'^users/register$', views.create),
	url(r'^users/logout$', views.logout)
]
