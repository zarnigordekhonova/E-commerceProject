from rest_framework import serializers

from apps.orders.models import Order, OrderDetail
from apps.orders.api_endpoints.CreateOrder.serializers import OrderDetailSerializer


class OrderHistorySerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(source="order_details", many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "total",
            "status",
            "shipping_type",
            "shipping_cost",
            "created_at",
            "order_detail"
        )

