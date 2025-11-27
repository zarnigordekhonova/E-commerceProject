from django.db import transaction

from rest_framework import serializers

from apps.products.models import (ProductVariant, 
                                  Option, 
                                  OptionValue, 
                                  ProductVariantOptionValue)


class OptionValueSerializer(serializers.Serializer):
    option_id = serializers.PrimaryKeyRelatedField(
        queryset = Option.objects.all(),
        source ="option"
    )
    value = serializers.CharField()


# fixed
class AddProductVariantSerializer(serializers.ModelSerializer):
    options = OptionValueSerializer(required=True, write_only=True, many=True)

    class Meta:
        model = ProductVariant
        fields = (
            "product",
            "sku_code",
            "stock_quantity",
            "price",
            "discount_price",
            "discount_percentage",
            "additional_info",
            "options"
        )
            
    def create(self, validated_data):
        options_data = validated_data.pop("options", [])

        product_variant = ProductVariant.objects.create(**validated_data)

        with transaction.atomic():
            for option_data in options_data:
                option = option_data.get('option', '')
                value_name = option_data.get('value', '').lower().strip()


                option_value, _ = OptionValue.objects.get_or_create(
                    option=option,
                    value=value_name
                )

                ProductVariantOptionValue.objects.create(
                    product_variant=product_variant,
                    option_value=option_value
                )
        
        return product_variant 