from django.conf.urls import url

from download import views


urlpatterns = [
    url(r'^(windows|mac-os-x|linux|for-developers)/$',
        views.download,
        name='download'),
    url(r'^$', views.download, name='download'),

]
