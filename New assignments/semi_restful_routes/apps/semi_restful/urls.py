from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.products),
	url(r'^new$', views.new),
	url(r'^(?P<id>\d+)/$', views.products_w_id),
	url(r'^edit/(?P<id>\d+)/$', views.edit),
	url(r'^destroy/(?P<id>\d+)/$', views.destroy)
]
