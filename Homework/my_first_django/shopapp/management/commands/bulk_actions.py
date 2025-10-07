"""
Добавление товара пачками
"""
from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk_actions")

        res = Product.objects.filter(
            name__contains="Smartphone",
        ).update(discount=10)
        print(res)

        # добавляет пачкой
        # info = [
        #     ("Smartphone 1", 199),
        #     ("Smartphone 2", 299),
        #     ("Smartphone 3", 399),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        # result = Product.objects.bulk_create(products)
        # for obj in result:
        #     print(obj)

        self.stdout.write("Dome")
