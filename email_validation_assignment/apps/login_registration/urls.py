from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='user_signin'),
	url(r'^login$', views.login, name='user_login'),
	url(r'^register$', views.create, name='user_register'),
	url(r'^logout$', views.logout, name='user_logout'),
	url(r'^(?P<id>\d+)$', views.show, name='user_show')
]
