from rest_framework import serializers

from apps.products.models import Category, Product
from apps.products.api_endpoints.ProductList.serializers import ProductImageSerializer


class ProductListByCategorySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
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

    def get_images(self, obj):
        """Gets the images of the first variant of the product."""
        first_variant = obj.variants.first()
        if first_variant:
            images = first_variant.images.all()
            return ProductImageSerializer(images, many=True).data
        return []

    def get_price(self, obj):
        first_variant = obj.variants.first()
        return first_variant.price if first_variant else None
    
    def get_discount_percentage(self, obj):
        first_variant = obj.variants.first()
        return first_variant.discount_percentage if first_variant else None
    