from django.conf.urls import url
from . import views
# Models--Views---Templates

urlpatterns = [
    url(r'^$', views.index)
]
