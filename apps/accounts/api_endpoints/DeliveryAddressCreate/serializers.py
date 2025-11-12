from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.accounts.models import UserDeliveryAddres

User =  get_user_model()


class DeliveryAddressSerializer(serializers.Serializer):
    class Meta:
        model = UserDeliveryAddres
        fields = (
            "country",
            "city",
            "street",
            "building_number",
            "is_default"
        )
        read_only_fields = (
            "created_at",
            "updated_at",
        )
