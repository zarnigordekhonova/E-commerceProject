from rest_framework import serializers

from apps.products.models import Option


class OptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ("id", "name")

        read_only_fields = ("id",)