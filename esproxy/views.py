from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


def login_or_404(func):
    def inner(*args, **karags):
        request = args[0]
        if request.user.is_authenticated():
            func(*args, **karags)
        else:
            #raise Http404
            return HttpResponseRedirect("/es/")

    return inner



@login_or_404
@csrf_exempt
def elasticsearch(request):
    fullpath = request.get_full_path()
    fullpath = fullpath[len("/elasticsearch"):]
    response = HttpResponse()
    response['X-Accel-Redirect'] = '/es/' + fullpath
    return response
