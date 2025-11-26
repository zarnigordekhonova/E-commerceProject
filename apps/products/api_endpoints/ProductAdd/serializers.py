from rest_framework import serializers

from apps.products.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug"
            "description",
            "is_new",
            "rating",
            "designed_year",
            "designed_by",
            "category",
            "show_with_posts"
        )

        read_only_fields = ("id", "slug", "rating", "designed_year")