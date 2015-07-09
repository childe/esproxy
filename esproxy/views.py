from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt


def login_required(func):
    def inner(*args, **karags):
        request = args[0]
        if request.user.is_authenticated():
            func(*args, **karags)
        else:
            raise Http404

    return inner



#@login_required
@csrf_exempt
def elasticsearch(request):
    fullpath = request.get_full_path()
    fullpath = fullpath.lstrip("/elasticsearch")
    response = HttpResponse()
    response['X-Accel-Redirect'] = '/es/' + fullpath
    return response
