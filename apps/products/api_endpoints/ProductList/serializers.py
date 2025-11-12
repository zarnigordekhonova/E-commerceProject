from rest_framework import serializers

from apps.products.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "image",
        )


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    designed_year = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", 
            "name",
            "designed_by",
            "designed_year",
            "images"
        )

    def get_designed_year(self, obj):
        return obj.designed_year.year if obj.designed_year else None
    


