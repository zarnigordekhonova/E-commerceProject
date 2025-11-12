from rest_framework import serializers

from apps.orders.models import ShoppingCart, ShoppingCartItem


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product.name', read_only=True)
    product_image = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(
        source='subtotal',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
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
        image = obj.product.product.images.first()
        return image.image.url if image else None


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = ShoppingCartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    is_empty = serializers.BooleanField(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = (
            "id",
            "items",
            "total_price",
            "is_empty"
        )
