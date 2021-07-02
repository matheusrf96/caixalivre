from django.urls import path
from django.urls.conf import include

from api.views import product_actions, customer_actions, register_purchase, seller_actions, get_sellers_commission

urlpatterns = [
    path('products', product_actions, name='api_products'),
    path('customers', customer_actions, name='api_customers'),
    path('sellers/', include([
        path('', seller_actions, name='api_sellers'),
        path('commission', get_sellers_commission, name='api_sellers_commision')
    ])),
    path('purchases', register_purchase, name='api_purchases'),
]
