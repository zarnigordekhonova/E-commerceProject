from django.urls import path

from apps.orders.api_endpoints import (
    AddToCartAPIView,
    CartDetailAPIView,
    RemoveFromCartAPIView,
    ClearCartAPIView,
    # Order
    OrderCreateAPIView,
    OrderCancelAPIView,
    OrderHistoryAPIView,
)

app_name="orders"

urlpatterns = [
    path("cart/add/", AddToCartAPIView.as_view(), name="add-to-cart"),
    path("cart/detail/", CartDetailAPIView.as_view(), name="cart-detail"),
    path("remove/<int:item_id>/cart/", RemoveFromCartAPIView.as_view(), name="remove-from-cart"),
    path("clear/cart/", ClearCartAPIView.as_view(), name="cart-clear"),
    # Order
    path("create/", OrderCreateAPIView.as_view(), name="order-create"),
    path("cancel/<int:order_id>/", OrderCancelAPIView.as_view(), name="order-cancel"),
    path("history/", OrderHistoryAPIView.as_view(), name="order-history"),
]