from rest_framework import serializers

from apps.orders.models import ShoppingCartItem


class AddToCartSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=False, default=1)


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product.name', read_only=True)
    product_image = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    is_in_stock = serializers.BooleanField(read_only=True) 

    class Meta:
        model = ShoppingCartItem
        fields = (
            "id",
            "product",
            "product_name",
            "product_image",
            "quantity",
            "subtotal",
            "is_in_stock"
        )

    def get_product_image(self, obj):
        image = obj.product.images.first()
        return image.image.url if image else None
    
    def get_subtotal(self, obj):
        return obj.subtotal
    
