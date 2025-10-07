"""
Вэтом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам и т.д.
"""
import logging
from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# для добавления в АПИ по продукту использукм
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .forms import GroupForm
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

log = logging.getLogger(__name__)

@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CRUD для сущностей товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        # print("hello product list")
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves product, return 404",
        responses={
        200: ProductSerializer,
        404: OpenApiResponse(description="Empty response, product by id not found"),
    }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        OrderingFilter, DjangoFilterBackend,
    ]
    filterset_fields = [
        "promocode",
        "user",
    ]
    ordering_fields = [
        "user",
        "promocode",
        "created_at",
    ]


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        print("shop index context", context)
        log.debug("Product for shop index: %s", products)
        log.info("Rendering shop index")
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupListView(LoginRequiredMixin, View):   # данный класс будет заменять group_list которая скрыта ниже
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


# ДЗ модуль 19
class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = "shopapp/users_orders_list.html"
    # queryset = (
    #     Order.objects
    #     .select_related("user")
    #     .prefetch_related("products")
    # )
    # model = Order

    def get_queryset(self):
        self.owner = get_object_or_404(User, id=self.kwargs["user_id"])
        # print(f"что то: {self.owner.pk} {self.owner}")
        # queryset = (Order.objects.select_related("user")
        #           .filter(user_id=self.kwargs["user_id"]))
        #
        # return queryset
        return Order.objects.select_related("user").filter(user_id=self.kwargs["user_id"])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["owner"] = self.owner
        data["time_running"] = default_timer()
        # print("вывод дата",data)
        return data


class OrderDetailView(DetailView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        return JsonResponse({"products": products_data})


class OrdersDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        order_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.pk,
                "products": [or_pr.pk for or_pr in order.products.all()],
            }
            for order in orders
        ]
        return JsonResponse({"orders": order_data})


# ДЗ модуль 19
class UserOrdersDataExportView(View):
    def get(self, request: HttpRequest, user_id):
        cache_key = f"user_orders_data_export {user_id}"
        serializer = cache.get(cache_key)
        print(cache_key)
        if serializer is None:
            user = get_object_or_404(User, id=user_id)
            print(user)
            orders = Order.objects.filter(user=user).prefetch_related("products").order_by("-pk").all()
            serializer = OrderSerializer(orders, many=True)
            cache.set(cache_key, serializer, 300)

        return JsonResponse({"orders": serializer.data})