from django.db import transaction

from rest_framework import serializers

from apps.orders.models import Order, OrderDetail, ShoppingCart
from apps.orders.utils import calculate_shipping_cost


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "country",
            "city",
            "state",
            "street",
            "zip_code",
            "payment_method"
        )


class OrderCreateSerializer(serializers.Serializer):
    shipping_type = serializers.ChoiceField(
        choices=Order.ShippingType.choices
    )
    order_detail = OrderDetailSerializer()

    def create(self, validated_data):
        user = self.context['request'].user
        shipping_type = validated_data['shipping_type']
        order_detail_data = validated_data['order_detail']

        # Get user's cart
        try:
            cart = ShoppingCart.objects.get(user=user)
        except ShoppingCart.DoesNotExist:
            raise serializers.ValidationError("Shopping cart not found.")

        if cart.is_empty:
            raise serializers.ValidationError("Cannot create order from empty cart.")

        shipping_cost = calculate_shipping_cost(shipping_type)

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                cart=cart,
                shipping_type=shipping_type,
                shipping_cost=shipping_cost,
                status=Order.OrderStatus.PENDING
            )

            order.total = cart.total_price + shipping_cost
            order.save(update_fields=['total'])

            order_detail = OrderDetail.objects.create(
                order=order,
                **order_detail_data
            )

            cart.clear()

        return order