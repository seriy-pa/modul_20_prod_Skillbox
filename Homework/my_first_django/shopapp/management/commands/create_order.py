from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Order, Product


class Command(BaseCommand):
    # transaction.atomic нужен для проведения транзакций если все ОК то операция проходит
    # если возникает ошибка то откатываются все задачи до момента начала операции
    @transaction.atomic
    def handle(self, *args, **options):

        # также можно использовать как
        # with transaction.atomic():
        #    ...

        self.stdout.write("Create order")
        user = User.objects.get(username="admin")
        # products: Sequence[Product] = Product.objects.all()
        # выгружаем все поля но некоторые будут выгружены когда к ним будет обращение
        # products: Sequence[Product] = Product.objects.defer("description", "price").all()
        # метод ONLY обратный методу DEFER выгружает все поля но отображает только указанные
        products: Sequence[Product] = Product.objects.only("id").all()
        order, created = Order.objects.get_or_create(
            delivery_address="ul Ivanova, d 8",
            promocode="promo4",
            user=user,
        )
        for product in products:
            order.products.add(product)
            order.save()
        self.stdout.write(f"Created order {order}")
