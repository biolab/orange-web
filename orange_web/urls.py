from django.conf.urls import patterns, url

from homepage import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^screenshots/$', views.screenshots, name='index'),
                       url(r'^license/$', views.license, name='license'),
                       url(r'^contributing-to-orange/$',
                           views.contribute, name='contribute'),
                       )
