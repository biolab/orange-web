from django.conf.urls import url

from error_report import views
urlpatterns = [
    url(r'^v1/$', views.v1, name='v1'),
]
