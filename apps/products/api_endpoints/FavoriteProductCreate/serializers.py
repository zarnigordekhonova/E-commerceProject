from rest_framework import serializers

from apps.products.models import ProductVariant, UserProductFavorite


class FavoriteProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "color",
            "price",
            "discount_percentage"
        )


class FavoriteProductCreateSerializer(serializers.ModelSerializer):
    product = FavoriteProductVariantSerializer(read_only=True)
    product_name = serializers.CharField(source="product.product.name", read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = UserProductFavorite
        fields = (
            "id",
            "product",
            "product_name",
            "product_image",
            "created_at"
        )

    def get_product_image(self, obj):
        image = obj.product.images.first()
        if image:
            return image.image.url
        return None