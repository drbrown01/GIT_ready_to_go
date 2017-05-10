from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^success$', views.show),
	url(r'^register$', views.create)
]
