from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^text-analysis/$', TemplateView.as_view(template_name='courses/text-analysis.html')),
]
