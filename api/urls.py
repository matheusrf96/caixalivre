from django.urls import path

from api.views import product_actions, customer_actions, register_purchase, seller_actions

urlpatterns = [
    path('products', product_actions, name='api_products'),
    path('customers', customer_actions, name='api_customers'),
    path('sellers', seller_actions, name='api_sellers'),
    path('purchases', register_purchase, name='api_purchases'),
]
