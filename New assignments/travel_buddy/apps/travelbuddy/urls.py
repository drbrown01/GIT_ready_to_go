from django.conf.urls import url, include
from . import views


urlpatterns =[
    url(r'^dashboard$', views.travel_index, name= 'travel_index'),
    url(r'^create$', views.add_item, name= 'add' ),
    url(r'^create_item$', views.create_item, name= 'create'),
    url(r'^logout$', views.logout, name= 'logout' ),
    url(r'^view/(?P<item_id>\d+)$', views.view_item, name= 'view'),
    #this way it will send the correct data (item_id) when it's rerouting
    url(r'^add/(?P<item_id>\d+)$', views.add_wishlist, name= 'add_wishlist'),
    url(r'^remove/(?P<item_id>\d+)$', views.remove_item, name= 'remove_item'),



]
