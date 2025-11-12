from rest_framework import serializers

from apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField()
    class Meta:
        model = Category
        fields = (
            "id",
            "category_name",
            "slug",
            "product_count",
            "created_at",
            "updated_at",
        )