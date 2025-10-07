from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupListView,

    ProductDetailsView,
    ProductsListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,

    ProductsDataExportView,
    OrdersDataExportView,

    OrdersListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,

    ProductViewSet,
    OrderViewSet,

    UserOrdersListView,
    UserOrdersDataExportView,

)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    # path("", cache_page(60 * 2)(ShopIndexView.as_view()), name="index"),
    path("", ShopIndexView.as_view(), name="index"),

    path("groups/", GroupListView.as_view(), name="group_list"),
    path("api/", include(routers.urls)),

    path("products/export/", ProductsDataExportView.as_view(), name="products-export"),
    path("orders/export/", OrdersDataExportView.as_view(), name="orders-export"),

    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),

    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),

    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="users_orders_list"),
    path("users/<int:user_id>/orders/export/", UserOrdersDataExportView.as_view(), name="user-orders-export"),
]
