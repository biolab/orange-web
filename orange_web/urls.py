"""Map URL requests to their respective functions or files."""
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from homepage import views


urlpatterns = \
    patterns('',
             url(r'^$', views.index, name='index'),
             url(r'^screenshots/$', views.screens, name='screenshots'),
             url(r'^getting-started/$', views.start, name='start'),
             url(r'^license/$', views.license, name='license'),
             url(r'^contributing/$', views.contribute, name='contribute'),
             url(r'^contact/$', views.contact, name='contact'),
             url(r'^download/$', views.download, name='download'),
             url(r'^download/(windows|mac-os-x|linux|for-developers)/$',
                 views.download,
                 name='download'),
             url(r'^community/$',
                 TemplateView.as_view(template_name='community.html'),
                 name='community'),
             url(r'^citation/$',
                 TemplateView.as_view(template_name='citation.html'),
                 name='citation'),
             url(r'^orange3/$',
                 TemplateView.as_view(template_name='orange3.html'),
                 name='orange3'),
             )
