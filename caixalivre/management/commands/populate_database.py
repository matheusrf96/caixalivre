import time
import requests
import json
import random

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populate database'

    def run_command(self):
        for i in range(5):
            data = {
                "product": {
                    "name": f"Produto { i }",
                    "price": round(random.uniform(10, 100), 2),
                }
            }
            requests.post('http://localhost:8000/api/products', json.dumps(data))

        for i in range(5):
            data = {
                "seller": {
                    "full_name": f"Vendedor { i }",
                }
            }
            requests.post('http://localhost:8000/api/sellers', json.dumps(data))

        for i in range(5):
            data = {
                "customer": {
                    "name": f"Cliente { i }",
                }
            }
            requests.post('http://localhost:8000/api/customers', json.dumps(data))

        data = {
            'purchase': {
                'customer': 5,
                'seller': 5,
                'products': [
                    {
                        'id': 5,
                        'quantity': 5,
                        'price': 50.00,
                        'commission': 5,
                    },
                    {
                        'id': 3,
                        'quantity': 3,
                        'price': 100.00,
                        'commission': 10,
                    },
                ]
            }
        }
        requests.post('http://localhost:8000/api/purchases', json.dumps(data))

    def handle(self, *args, **options):
        begin = time.time()

        print('Running...')

        self.run_command()

        print('\nSuccess! :)')
        print(f'Done with {time.time() - begin}s')
