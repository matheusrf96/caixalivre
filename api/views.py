import json

from django.shortcuts import HttpResponse


# Create your views here.
def hello(request):
    return HttpResponse(json.dumps({'msg': 'hello!'}), content_type='application/json')
