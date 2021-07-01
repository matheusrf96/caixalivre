from django.urls import path, include

from api.views import hello

urlpatterns = [
    path('hello', hello, name='api_hello'),
]
