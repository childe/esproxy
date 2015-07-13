from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django_cas.views import login,logout
from settings import URL_PREFIX

urlpatterns = patterns(
    '',
    url(r'^(%s)$'%URL_PREFIX, 'esproxy.views.home'),
    url(r'^(%s)index.html'%URL_PREFIX, 'esproxy.views.home'),
    url(r'^(%s)login.html/$'%URL_PREFIX, csrf_exempt(login)),
    url(r'^(%s)logout.html/$'%URL_PREFIX,logout),

    url(r'^(%s)elasticsearch/'%URL_PREFIX, 'esproxy.views.elasticsearch'),

    url(r'^(%s)admin/'%URL_PREFIX, include(admin.site.urls)),
)
