# -*- coding: utf-8 -*-
import os
import re
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import auth
from django.core.cache import cache
from esauth.models import ESAuth
import settings


def pass_authorize(user_config_list, method, path):
    '''if the USER could do the method with the path.
    if he has the permission, return True
    Nontice is he do NOT has permission, return **config** which will be user later
    '''
    for config in user_config_list:
        if config.get_request_method_display() in ("_ALL_", method) and re.match(config.uri_regexp, path):
            if config.allowed is True:
                return True
            else:
                return config
    return True


def _config_sort_method(x, y):
    if x.index != y.index:
        return int(x.index - y.index)

    if x.username != "":
        if x.username != "_ALL_":
            x_factor = 1
        else:
            x_factor = 2
    else:
        x_factor = 3

    if y.username != "":
        if y.username != "_ALL_":
            y_factor = 1
        else:
            y_factor = 2
    else:
        y_factor = 3

    return x_factor - y_factor


def authorize(func):
    def inner(*args, **karags):

        request = args[0]
        user = request.user
        path = request.path
        path = path.replace('/'+settings.ELASTICSEARCH_PROXY, "", 1)
        method = request.method

# sort configs && build cache
        user_config_list = cache.get(user.username)
        if user_config_list is None:
            user_config_list = []
            for o in ESAuth.objects.order_by("index"):
                if o.username == user.username or o.username == "_ALL_" or o.group in [e.name for e in user.groups.all()]:
                    user_config_list.append(o)

            user_config_list.sort(cmp=_config_sort_method)
            cache.set(
                user.username,
                user_config_list,
                settings.AUTH_CACHE_TIMEOUT)

# process _msearch
        action = [e for e in path.split('/') if e and e[0] == '_']

        if action and action[0] == '_msearch':
            _splited = [e for e in path.split('/')]
            indices = _splited[_splited.index('_msearch')-1].split(',')
            for i, line in enumerate(request.body.split('\n')):
                if i % 2 == 0 and line != "":
                    indices.extend(json.loads(line).get('index').split(','))
            path = '/' + ','.join(indices) + '/_search'

        rst = pass_authorize(user_config_list, method, path)
        if rst is True:
            return func(*args, **karags)
        else:
            # TODO: 301/302
            response = HttpResponse(
                rst.response_value,
                content_type="application/json; charset=UTF-8")
            response.status_code = rst.response_code
            return response

    return inner


def login_or_redirect_to_internal(func):
    def inner(*args, **karags):
        request = args[0]
        if request.user.is_authenticated():
            return func(*args, **karags)
        else:
            r = HttpResponse('',)
            r.status_code = 403
            return r

    return inner


@authorize
@login_or_redirect_to_internal
@csrf_exempt
def elasticsearch(request):
    fullpath = request.get_full_path().encode("UTF8")
    response = HttpResponse()
    response[
        'X-Accel-Redirect'] = fullpath.replace(settings.ELASTICSEARCH_PROXY, settings.ELASTICSEARCH_REAL, 1)
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
