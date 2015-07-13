import os
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from settings import ELASTICSEARCH_PROXY, ELASTICSEARCH_REAL,KIBANA_DIR


def login_or_404(func):
    def inner(*args, **karags):
        request = args[0]
        if request.user.is_authenticated():
            return func(*args, **karags)
        else:
            return HttpResponseRedirect("/es/")

    return inner


#@login_or_404
@csrf_exempt
def elasticsearch(request):
    fullpath = request.get_full_path()
    fullpath = fullpath[len(ELASTICSEARCH_PROXY):]
    response = HttpResponse()
    response['X-Accel-Redirect'] = ELASTICSEARCH_REAL + '/' + fullpath
    return response


def home(request):
    return HttpResponseRedirect("index.html")

@login_required
def index(request):
    html = open(os.path.join(KIBANA_DIR,"index.html")).read()
    return HttpResponse(html)

