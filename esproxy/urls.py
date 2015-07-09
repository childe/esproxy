from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django_cas.views import login,logout

urlpatterns = patterns(
    '',
    url(r'^$', 'esproxy.views.home'),
    url(r'^elasticsearch/', 'esproxy.views.elasticsearch'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login.html/$', csrf_exempt(login)),
    url(r'^logout.html/$',logout),
)
