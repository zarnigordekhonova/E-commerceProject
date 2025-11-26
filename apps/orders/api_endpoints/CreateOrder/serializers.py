from django.db import transaction

from rest_framework import serializers

from apps.orders.models import Order, ShoppingCartItem, OrderItem
from apps.orders.utils import calculate_shipping_cost


class OrderCreateSerializer(serializers.ModelSerializer):
    shipping_type = serializers.ChoiceField(
        choices=Order.ShippingType.choices
    )
    class Meta:
        model = Order
        fields = (
            "shipping_type",
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

    def create(self, validated_data):
        user = self.context['request'].user
        shipping_type = validated_data.pop('shipping_type')
        
        cart_items = ShoppingCartItem.objects.filter(user=user)

        if not cart_items.exists():
            raise serializers.ValidationError("Cannot create order from empty cart.")

        shipping_cost = calculate_shipping_cost(shipping_type)

        with transaction.atomic():
            items_total = sum(item.subtotal for item in cart_items)

            if shipping_type == Order.ShippingType.FREE:
                total_price = items_total
            else:
                total_price = items_total + shipping_cost

            order = Order.objects.create(
                user=user,
                shipping_type=shipping_type,
                shipping_cost=shipping_cost,
                total_price=total_price,
                status = Order.OrderStatus.PENDING,
                **validated_data
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            cart_items.delete()
            print("CART HAS BEEN CLEARED")
        
        return order

