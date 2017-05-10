from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.index),
	url(r'^home$', views.home),
	url(r'^login/process$', views.login),
	url(r'^register/process$', views.register),
	url(r'^additem$', views.additem),
	url(r'^additem/process$', views.additemprocess),
	url(r'^display/(?P<id>\d+)$', views.displayitem),
	url(r'^delete/(?P<id>\d+)$', views.deleteitem),
	url(r'^remove/(?P<id>\d+)$', views.removeitem),
	url(r'^addthis/(?P<id>\d+)$', views.addthis),


	url(r'^log_out$', views.log_out),

]
