import json
from datetime import datetime, timedelta
from decimal import Decimal

from django.shortcuts import HttpResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from api.models import Product, Customer, Seller, Purchase, PurchaseProducts
from api.decorators import add_cors_react_dev


# Views de produtos
def get_products(name):
    if not name:
        return [{
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
        } for product in Product.objects.filter(active=True)]

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
            return (5.0 / 100)
        return (commission / 100)

    if commission < 4.0:
        return (4.0 / 100)

    if commission == 0:
        return 0.0

    return (commission / 100)


def create_product(product):
    product = {
        'name': product.get('name') or 'Sem Nome',
        'price': product.get('price') or 0.0,
    }

    Product(**product).save()
    return Product.objects.last()


@require_http_methods(["GET", "POST"])
@add_cors_react_dev
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
    if not name:
        return [{
            'id': customer.id,
            'name': customer.name,
        } for customer in Customer.objects.filter(active=True)]

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
@add_cors_react_dev
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
    if not name:
        return [{
            'id': seller.id,
            'name': seller.full_name,
        } for seller in Seller.objects.filter(active=True)]

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
@add_cors_react_dev
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
@add_cors_react_dev
def register_purchase(request):
    data = json.loads(request.body).get('purchase')

    if not data:
        raise Exception('Não há dados de venda')
    if not data.get('products'):
        raise Exception('Não há dados de produto')

    purchase_data = {
        'price': 0.0,
        'customer_id': data.get('customer'),
        'seller_id': data.get('seller'),
    }

    Purchase(**purchase_data).save()
    purchase = Purchase.objects.last()

    for product in data.get('products'):
        purchase.price += Decimal(product.get('price') * product.get('quantity'))

        PurchaseProducts(
            purchase_id=purchase.id,
            product_id=product.get('id'),
            quantity=product.get('quantity'),
            commission=(
                calc_commission(product.get('commission') or 0.0)
                * (product.get('price') or 0.0)
                * product.get('quantity')
            ),
        ).save()

        purchase.save()

    return HttpResponse(
        json.dumps({'msg': f'Pedido cadastrado (#{ purchase.id })'}),
        content_type='application/json',
        status=201,
    )


@require_GET
@add_cors_react_dev
def get_sellers_commission(request):
    data = request.GET

    seller_id = data.get('seller')

    if not seller_id:
        return HttpResponse(
            json.dumps({'msg': 'O ID do vendedor não foi inserido'}),
            content_type='application/json',
            status=400,
        )

    begin = datetime.now() - timedelta(days=1)
    end = datetime.now()

    if data.get('begin_date'):
        begin = datetime.strptime(data.get('begin_date'), '%Y-%m-%d')
    if data.get('end_date'):
        end = datetime.strptime(data.get('end_date'), '%Y-%m-%d')

    if begin == end:
        end += timedelta(days=1) - timedelta(seconds=1)
    elif end < begin:
        aux = begin
        begin = end
        end = aux

    commission = PurchaseProducts.objects.filter(
        created_at__gte=begin,
        created_at__lte=end,
        purchase__seller_id=seller_id,
        purchase__seller__active=True,
    ).aggregate(Sum('commission'))

    if not commission.get('commission__sum'):
        return HttpResponse(
            json.dumps({
                'msg': 'O vendedor não existe ou não possui comissão para este período',
                'seller_id': seller_id,
                'commission': 0.0,
            }),
            content_type='application/json',
            status=404,
        )

    return HttpResponse(
        json.dumps({
            'seller_id': seller_id,
            'commission': float(commission.get('commission__sum')),
        }),
        content_type='application/json',
    )
