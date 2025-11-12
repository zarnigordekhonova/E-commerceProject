from rest_framework import serializers

from apps.products.models import Product, ProductVariant, ProductComment, ProductRating
from apps.products.api_endpoints.ProductList.serializers import ProductImageSerializer


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "color",
            "additional_info",
            "measurement",
            "sku_code",
            "price",
            "discount_price",
            "discount_percentage"
        )


class ProductCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.full_name", read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = ProductComment
        fields = (
            "id",
            "user",
            "comment",
            "rating",
            "created_at"
        )

    def get_rating(self, obj):
        try:
            product_rating = ProductRating.objects.get(
                user=obj.user,
                product=obj.product
            )
            return product_rating.rating
        except ProductRating.DoesNotExist:
            return None
        

class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.category_name", read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ProductCommentSerializer(source="product_comment", many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "images",
            "reviews_number",
            "name",
            "description",
            "rating",
            "is_new",
            "category",
            "variants",
            "reviews"
        )
