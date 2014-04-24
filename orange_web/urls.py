from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from homepage import views

urlpatterns = \
    patterns('',
             url(r'^$', views.index, name='index'),
             url(r'^screenshots/$', views.screenshots, name='screenshots'),
             url(r'^license/$', views.license, name='license'),
             url(r'^contributing/$', views.contribute, name='contribute'),
             url(r'^download/$', views.download, name='download'),
             url(r'^community/$', views.community, name='community'),
            )