from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('apps.time_display.urls'))
]
