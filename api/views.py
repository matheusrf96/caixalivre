import json
from datetime import datetime

from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods

from api.models import Product, Customer


# Views de produtos
def get_products(name):
    products = [product.name for product in Product.objects.filter(name__contains=name, active=True)]
    return products


def calc_commission(commission):
    dt = datetime.now()
    reference_time = datetime(dt.year, dt.month, dt.day, 12, 0, 0)

    if datetime.now().hour <= reference_time:
        if commission > 5.0:
            return 5.0
        return commission

    if commission < 4.0:
        return 4.0
    return commission


def create_product(product):
    product = {
        'name': product.get('name') or 'Sem Nome',
        'price': product.get('price') or 0.0,
        'commission': calc_commission(product.get('commission') or 0.0),
    }

    Product(**product).save()
    return Product.objects.last()


@require_http_methods(["GET", "POST"])
def product_actions(request):
    if request.method == 'GET':
        products = get_products(request.GET.get('name'))
        return HttpResponse(json.dumps({'products': products}), content_type='application/json')

    product = create_product(request.POST.get('product'))
    return HttpResponse(
        json.dumps({'msg': f'Produto cadastrado (#{ product.id }: { product.name })'}),
        content_type='application/json',
        status=201,
    )


# Views de clientes
def get_customers(name):
    customers = [customer.name for customer in Customer.objects.filter(name__contains=name, active=True)]
    return customers


def create_customer(customer):
    customer = {
        'name': customer.get('name') or 'Sem nome',
        'description': customer.get('description'),
    }

    Customer(**customer).save()
    return Customer.objects.last()


@require_http_methods(["GET", "POST"])
def customer_actions(request):
    if request.method == 'GET':
        customers = get_customers(request.GET.get('name'))
        return HttpResponse(json.dumps({'customers': customers}), content_type='application/json')

    customer = create_product(request.POST.get('customer'))
    return HttpResponse(
        json.dumps({'msg': f'Cliente cadastrado (#{ customer.id }: { customer.name })'}),
        content_type='application/json',
        status=201,
    )
