from django.conf.urls import url

from download import views


urlpatterns = [
    url(r'^$', views.download, name='download'),
    url(r'^windows/$', views.download_windows, name='download/windows'),
    url(r'^macos/$', views.download_macos, name='download'),
    url(r'^linux/$', views.download_linux, name='download'),
    url(r'^$', views.download, name='download'),

]
