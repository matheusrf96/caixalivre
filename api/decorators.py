
from django.http import HttpResponse
from django.conf import settings


def add_cors_react_dev(func):
    def add_cors_react_dev_response(response):
        if settings.DEBUG:
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, *'
        return response

    def inner(request, *args, **kwargs):
        if request and request.method == 'OPTIONS':
            return add_cors_react_dev_response(HttpResponse('Ok'))

        result = add_cors_react_dev_response(func(request, *args, **kwargs))
        return result

    return inner
