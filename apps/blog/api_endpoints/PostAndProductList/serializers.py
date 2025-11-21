from rest_framework import serializers

from apps.products.models import Product


class ProductMinimalSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    designed_year = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", 
            "name",
            "designed_by",
            "designed_year",
            "image",
        )

    def get_designed_year(self, obj):
        return obj.designed_year.year if obj.designed_year else None
    
    def get_image(self, obj):
        variant = obj.variants.first()
        if variant:
            product_image = variant.images.first()
            if product_image:
                return product_image.image.url
        return None