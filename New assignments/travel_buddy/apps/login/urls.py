from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.login_index, name= 'user_index'),
    url(r'^register$', views.register, name= 'register'),
    url(r'^login$', views.login, name= 'login'),

]
