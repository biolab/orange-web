from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^text-analysis/$', TemplateView.as_view(template_name='courses/text-analysis.html')),
    url(r'^digital-humanities-2017/$', TemplateView.as_view(template_name='courses/digital-humanities-2017.html')),
    url(r'^introduction-to-data-mining/$', TemplateView.as_view(template_name='courses/introduction-to-data-mining.html')),
]
