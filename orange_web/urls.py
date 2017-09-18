"""Map URL requests to their respective functions or files."""
import os

from django.conf import settings
from django.conf.urls import url, include
from django.views.generic import TemplateView

from homepage import views as homepage_views
from download import views as download_views


urlpatterns = [
    url(r'^$', homepage_views.index, name='index'),
    url(r'^screenshots/$', homepage_views.screens, name='screenshots'),
    url(r'^getting-started/$', homepage_views.start, name='start'),
    url(r'^license/$', homepage_views.license_page, name='license'),
    url(r'^privacy/$', homepage_views.privacy, name='privacy'),
    url(r'^contributing/$', homepage_views.contribute, name='contribute'),
    url(r'^contact/$', homepage_views.contact, name='contact'),
    url(r'^toolbox/$', homepage_views.toolbox, name='toolbox'),
    url(r'^faq/$',
        TemplateView.as_view(template_name='faq.html'),
        name='faq'),
    url(r'^community/$',
        TemplateView.as_view(template_name='community.html'),
        name='community'),
    url(r'^citation/$',
        TemplateView.as_view(template_name='citation.html'),
        name='citation'),
    url(r'^orange3/$',
        TemplateView.as_view(template_name='orange3.html'),
        name='orange3'),
    url(r'^orange2/$',
        TemplateView.as_view(template_name='download/orange2.html'),
        name='orange2'),
    url(r'^docs/$',
        TemplateView.as_view(template_name='docs.html'),
        name='docs'),
    url(r'^thank-you/$',
            TemplateView.as_view(template_name='thank-you.html'),
            name='thank-you'),
    url(r'^download/', include('download.urls')),
    url(r'^courses/', include('courses.urls')),
    url(r'^version/$', download_views.latest_version, name='version'),
    url(r'^error_report/', include('error_report.urls')),
]

# Check the features folder. Add every template that it finds in it.
feature_templates_dir = os.path.join(settings.BASE_DIR, 'homepage',
                                     'templates', 'features')
for fp in os.listdir(feature_templates_dir):
    # Template's file path
    tp = os.path.join(feature_templates_dir, fp)
    # Create stub from filename by removing '.html'
    stub = r'^features/{0}/$'.format(fp[:-5])
    # Add to urlpatterns list
    urlpatterns.append(url(stub, TemplateView.as_view(template_name=tp),))
