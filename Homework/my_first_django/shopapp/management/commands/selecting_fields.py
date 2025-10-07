from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")

        # выгружаем нужные данные кортежем
        # users_info = User.objects.values_list('pk', "username")
        # выгружает со скобками
        # users_info = User.objects.values_list("username")
        # делаем без
        users_info = User.objects.values_list("username", flat=True)
        print(list(users_info))
        for users_i in users_info:
            print(users_i)

        # выгружаем нужные данные ссловарем
        # products_values = Product.objects.values("pk", "name")
        # for p_values in products_values:
        #     print(p_values)

        self.stdout.write("Dome")
