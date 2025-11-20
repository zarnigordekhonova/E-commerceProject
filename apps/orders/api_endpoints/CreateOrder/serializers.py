from django.db import transaction

from rest_framework import serializers

from apps.orders.models import Order, OrderDetail, ShoppingCartItem, OrderItem
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
                status = Order.OrderStatus.PENDING
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            order_detail = OrderDetail.objects.create(
                order=order,
                **order_detail_data
            )

            cart_items.delete()
            print("CART HAS BEEN CLEARED")
        
        return order

