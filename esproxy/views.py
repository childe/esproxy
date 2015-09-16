# -*- coding: utf-8 -*-
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import auth
from .settings import ELASTICSEARCH_PROXY, ELASTICSEARCH_REAL, KIBANA_DIR, ELASTICSEARCH_AUTHORIZATION


def pass_authorize(username, index, config):
    for index_prefix, c in config.items():
        if not index.startswith(index_prefix):
            continue
        if username in c.get("allow", []):
            continue
        deny = c.get("deny", [])
        if deny == "all" or username in deny:
            return False
    return True


def authorize(func):
    def inner(*args, **karags):
        request = args[0]
        username = request.user.username
        fullpath = request.get_full_path()
        print fullpath
        action = [e for e in fullpath.split('/') if e and e[0] == '_']
        print action
        if action == [] or action[0] not in ELASTICSEARCH_AUTHORIZATION:
            return func(*args, **karags)

        action = action[0]
        indices = fullpath.split('/')[2].split(',')
        print indices
        for index in indices:
            if pass_authorize(username, index, ELASTICSEARCH_AUTHORIZATION[action]) is False:
                return HttpResponseRedirect(ELASTICSEARCH_REAL)

        return func(*args, **karags)

    return inner


def login_or_redirect_to_internal(func):
    def inner(*args, **karags):
        request = args[0]
        if request.user.is_authenticated():
            return func(*args, **karags)
        else:
            return HttpResponseRedirect(ELASTICSEARCH_REAL)

    return inner


@authorize
@login_or_redirect_to_internal
@csrf_exempt
def elasticsearch(request):
    fullpath = request.get_full_path().encode("UTF8")
    fullpath = fullpath[len(ELASTICSEARCH_PROXY):]
    response = HttpResponse("OK")
    response['X-Accel-Redirect'] = ELASTICSEARCH_REAL + '/' + fullpath
    response['Django-User'] = request.user.username
    return response


@login_required
def home(request):
    # return HttpResponseRedirect("index.html")
    html = open(os.path.join(KIBANA_DIR, "index.html")).read()
    response = HttpResponse(html)
    return response


def login(request):
    username = ""
    password = ""
    user = authenticate(username=username, password=password)
    auth.login(request, user)
    return HttpResponse("welcome " + user.username)


def logout(request):
    response = HttpResponse("OK")
    return response
