from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

try:
    from settings import AUTHENTICATION_BACKENDS
    if 'django_cas.backends.CASBackend' in AUTHENTICATION_BACKENDS:
        from django_cas.views import login as loginpage,logout
    else:
        raise
except:
    from esproxy.views import loginpage,logout
from esproxy.views import loginuser

urlpatterns = patterns(
    '',
    url(r'^$', 'esproxy.views.home'),
    url(r'^index.html', 'esproxy.views.home'),
    url(r'^elasticsearch/', 'esproxy.views.elasticsearch'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login.html$', loginpage),
    url(r'^login$', csrf_exempt(loginuser)),
    url(r'^logout$',logout),
)
