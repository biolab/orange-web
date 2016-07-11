"""Map URL requests to their respective functions or files."""
import os

from django.conf import settings
from django.conf.urls import url
from django.views.generic import TemplateView

from homepage import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^screenshots/$', views.screens, name='screenshots'),
    url(r'^getting-started/$', views.start, name='start'),
    url(r'^license/$', views.license_page, name='license'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^contributing/$', views.contribute, name='contribute'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^download/$', views.download, name='download'),
    url(r'^toolbox/$', views.toolbox, name='toolbox'),
    url(r'^download/(windows|mac-os-x|linux|for-developers)/$',
        views.download,
        name='download'),
    url(r'^community/$',
        TemplateView.as_view(template_name='community.html'),
        name='community'),
    url(r'^version/$', views.latest_version, name='version'),
    url(r'^citation/$',
        TemplateView.as_view(template_name='citation.html'),
        name='citation'),
    url(r'^orange3/$',
        TemplateView.as_view(template_name='orange3.html'),
        name='orange3'),
    url(r'^orange2/$',
        TemplateView.as_view(template_name='orange2.html'),
        name='orange2'),
    url(r'^docs/$',
        TemplateView.as_view(template_name='docs.html'),
        name='docs'),
]

# Check the feature_templates folder. Add every template that it finds in it.
feature_templates_dir = os.path.join(settings.BASE_DIR, 'homepage',
                                     'templates', 'feature_templates')
for fp in os.listdir(feature_templates_dir):
    # Template's file path
    tp = os.path.join(feature_templates_dir, fp)
    # Create stub from filename by removing '.html'
    stub = r'^{0}/$'.format(fp[:-5])
    # Add to urlpatterns list
    urlpatterns.append(url(stub, TemplateView.as_view(template_name=tp),))
