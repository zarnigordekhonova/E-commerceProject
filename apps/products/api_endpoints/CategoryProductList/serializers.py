from rest_framework import serializers

from apps.products.models import Category, Product
from apps.products.api_endpoints.ProductList.serializers import ProductImageSerializer


class ProductListByCategorySerializer(serializers.Serializer):
    images = ProductImageSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "images",
            "price",
            "discount_percentage",
            "rating"
        )

    def get_price(self, obj):
        first_variant = obj.variants.first()
        return first_variant.price if first_variant else None
    
    def get_discount_percentage(self, obj):
        first_variant = obj.variants.first()
        return first_variant.discount_percentage if first_variant else None
    