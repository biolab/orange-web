from django.conf.urls import url

from telemetry import views
urlpatterns = [
    url(r'^v1/$', views.v1, name='v1'),
]
