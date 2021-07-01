from django.urls import path

from api.views import product_actions

urlpatterns = [
    path('products', product_actions, name='api_products')
]
