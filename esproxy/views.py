from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from settings import ELASTICSEARCH_PROXY, ELASTICSEARCH_REAL


def login_or_404(func):
    def inner(*args, **karags):
        request = args[0]
        if request.user.is_authenticated():
            func(*args, **karags)
        else:
            return HttpResponseRedirect("/es/")

    return inner


@login_or_404
@csrf_exempt
def elasticsearch(request):
    fullpath = request.get_full_path()
    fullpath = fullpath[len(ELASTICSEARCH_PROXY):]
    response = HttpResponse()
    response['X-Accel-Redirect'] = ELASTICSEARCH_REAL + '/' + fullpath
    return response
