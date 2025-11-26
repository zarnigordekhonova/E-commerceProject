from rest_framework import serializers

from apps.orders.models import Order


class OrderHistorySerializer(serializers.ModelSerializer):
    order_detail = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "total_price",
            "status",
            "shipping_type",
            "shipping_cost",
            "created_at",
            "order_detail"
        )

    def get_order_detail(self, obj):
        return {
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "phone_number": obj.phone_number,
            "email": obj.email,
            "country": obj.country.id,
            "city": obj.city.id,
            "state": obj.state,
            "street": obj.street,
            "zip_code": obj.zip_code,
            "payment_method": obj.payment_method
        }
