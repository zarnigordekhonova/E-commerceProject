from rest_framework import serializers

from apps.products.models import Option


class OptionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            "id",
            "name"
        )