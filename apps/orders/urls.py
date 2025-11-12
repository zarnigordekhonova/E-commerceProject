from django.urls import path

from apps.orders.api_endpoints import (
    AddToCartAPIView,
    CartDetailAPIView,
    RemoveFromCartAPIView
)

app_name="orders"

urlpatterns = [
    path("cart/add/", AddToCartAPIView.as_view(), name="add-to-cart"),
    path("cart/detail/", CartDetailAPIView.as_view(), name="cart-detail"),
    path("remove/<int:pk>/cart/", RemoveFromCartAPIView.as_view(), name="remove-from-cart"),
]