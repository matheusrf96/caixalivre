import json
from datetime import datetime

from django.shortcuts import HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt

from api.models import Product, Customer, Seller, Purchase, PurchaseProducts


# Views de produtos
def get_products(name):
    products = [{
        'id': product.id,
        'name': product.name,
        'price': float(product.price),
    } for product in Product.objects.filter(name__icontains=name, active=True)]
    return products


def calc_commission(commission):
    dt = datetime.now()
    reference_time = datetime(dt.year, dt.month, dt.day, 12, 0, 0)

    if datetime.now().hour <= reference_time.hour:
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
    }

    Product(**product).save()
    return Product.objects.last()


@require_http_methods(["GET", "POST"])
@csrf_exempt
def product_actions(request):
    if request.method == 'GET':
        products = get_products(request.GET.get('name'))
        return HttpResponse(json.dumps({'products': products}), content_type='application/json')

    product = create_product(json.loads(request.body).get('product'))
    return HttpResponse(
        json.dumps({'msg': f'Produto cadastrado (#{ product.id }: { product.name })'}),
        content_type='application/json',
        status=201,
    )


# Views de clientes
def get_customers(name):
    customers = [{
        'id': customer.id,
        'name': customer.name,
    } for customer in Customer.objects.filter(name__icontains=name, active=True)]
    return customers


def create_customer(customer):
    customer = {
        'name': customer.get('name') or 'Sem nome',
        'description': customer.get('description'),
    }

    Customer(**customer).save()
    return Customer.objects.last()


@require_http_methods(["GET", "POST"])
@csrf_exempt
def customer_actions(request):
    if request.method == 'GET':
        customers = get_customers(request.GET.get('name'))
        return HttpResponse(json.dumps({'customers': customers}), content_type='application/json')

    customer = create_customer(json.loads(request.body).get('customer'))
    return HttpResponse(
        json.dumps({'msg': f'Cliente cadastrado (#{ customer.id }: { customer.name })'}),
        content_type='application/json',
        status=201,
    )


# Views de vendedores
def get_sellers(name):
    sellers = [{
        'id': seller.id,
        'name': seller.full_name,
    } for seller in Seller.objects.filter(full_name__icontains=name, active=True)]
    return sellers


def create_seller(seller):
    seller = {
        'full_name': seller.get('full_name') or 'Sem nome',
    }

    Seller(**seller).save()
    return Seller.objects.last()


@require_http_methods(["GET", "POST"])
@csrf_exempt
def seller_actions(request):
    if request.method == 'GET':
        sellers = get_sellers(request.GET.get('name'))
        return HttpResponse(json.dumps({'sellers': sellers}), content_type='application/json')

    seller = create_seller(json.loads(request.body).get('seller'))
    return HttpResponse(
        json.dumps({'msg': f'Vendedor cadastrado (#{ seller.id }: { seller.full_name })'}),
        content_type='application/json',
        status=201,
    )


# Views de venda
@require_POST
@csrf_exempt
def register_purchase(request):
    data = json.loads(request.body).get('purchase')

    if not data.get('purchase'):
        raise Exception('Não há dados de venda')
    if not data.get('products'):
        raise Exception('Não há dados de produto')

    purchase_data = {
        'price': data.get('price'),
        'customer': data.get('customer'),
        'seller': data.get('seller'),
    }

    Purchase(**purchase_data).save()
    purchase = Purchase.objects.last()

    products_data = [{
        'id': product.get('id'),
        'quantity': product.get('quantity'),
        'commission_value': (
            calc_commission(product.get('commission') or 0.0) * (product.get('price') or 0.0) * product.get('quantity')
        ),
    } for product in data.get('products')]

    for product in products_data:
        PurchaseProducts(
            purchase=purchase.id,
            product=product.get('id'),
            quantity=product.get('quantity'),
            commission=product.get('commission_value'),
        ).save()

    return HttpResponse(
        json.dumps({'msg': f'Pedido cadastrado (#{ purchase.id })'}),
        content_type='application/json',
        status=201,
    )
