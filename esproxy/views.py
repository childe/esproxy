# -*- coding: utf-8 -*-
import os
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import auth
import settings


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
        path = request.path
        action = [e for e in path.split('/') if e and e[0] == '_']
        if action == [] or action[0] not in settings.ELASTICSEARCH_AUTHORIZATION:
            return func(*args, **karags)

        action = action[0]
        if action == '_msearch':
            indices = json.loads(request.body.split('\n')[0])['index']
            if isinstance(indices, basestring):
                indices = [indices]
        else:
            indices = path.split('/')[2].split(',')
        for index in indices:
            if pass_authorize(username, index, settings.ELASTICSEARCH_AUTHORIZATION[action]) is False:
                return HttpResponseRedirect(settings.ELASTICSEARCH_REAL)

        return func(*args, **karags)

    return inner


def login_or_redirect_to_internal(func):
    def inner(*args, **karags):
        request = args[0]
        if request.user.is_authenticated():
            return func(*args, **karags)
        else:
            return HttpResponseRedirect(settings.ELASTICSEARCH_REAL)

    return inner


@authorize
@login_or_redirect_to_internal
@csrf_exempt
def elasticsearch(request):
    fullpath = request.get_full_path().encode("UTF8")
    fullpath = fullpath[len(settings.ELASTICSEARCH_PROXY):]
    response = HttpResponse("OK")
    response['X-Accel-Redirect'] = settings.ELASTICSEARCH_REAL + '/' + fullpath
    response['Django-User'] = request.user.username
    return response


@login_required
def home(request):
    html = open(os.path.join(settings.KIBANA_DIR, "index.html")).read()
    response = HttpResponse(html)
    return response


def loginpage(request):
    return render(
        request, 'login.html', {
            'next': request.GET.get(
                'next', '/')})


def loginuser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    nextpage = request.POST.get('next', '/')
    user = authenticate(username=username, password=password)
    if not user:
        return HttpResponseRedirect(nextpage)

    auth.login(request, user)
    return HttpResponseRedirect(nextpage)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
