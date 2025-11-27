from rest_framework import serializers

from apps.products.models import (Product, 
                                  ProductVariant, 
                                  ProductComment, 
                                  ProductRating,
                                  ProductVariantOptionValue)
from apps.products.api_endpoints.ProductList.serializers import ProductImageSerializer


class OptionValueSerializer(serializers.Serializer):
    option = serializers.CharField(source='option_value.option.name', read_only=True)
    value = serializers.CharField(source='option_value.value', read_only=True)


class ProductVariantSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "sku_code",
            "price",
            "discount_price",
            "discount_percentage",
            "stock_quantity",
            "additional_info",
            "options",
            "images"
        )

    def get_options(self, obj):
        variant_options = obj.variant_options.all()
        return OptionValueSerializer(variant_options, many=True).data


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
    category = serializers.SerializerMethodField()
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews_number = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "reviews_number",
            "name",
            "description",
            "rating",
            "is_new",
            "category",
            "variants",
        )

    def get_reviews_number(self, obj):
        return obj.product_comment.count()
    
    # fixed
    def get_category(self, obj):
        return {
            "id" : obj.category.id,
            "category_name": obj.category.category_name
        }
    
    
    


