from django.conf.urls import patterns, include, url

from homepage import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'orange_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^screenshots/$', views.screenshots, name='index'),
    url(r'^license/$', views.license, name='license'),
    url(r'^contributing-to-orange/$', views.contribute, name='contribute'),
)
