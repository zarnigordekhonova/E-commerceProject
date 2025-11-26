from django.db import transaction

from rest_framework import serializers

from apps.products.models import (ProductVariant, 
                                  Option, 
                                  OptionValue, 
                                  ProductVariantOptionValue)


class AddProductVariantSerializer(serializers.ModelSerializer):
    options = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=True
    )

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

    # Admin database da mavjud option ni kirityaptimi yo'qmi - shuni tekshiradi
    def validate_options(self, value):
        if not value:
            return value
        
        for option_data in value:
            option_name = option_data.get("option", '').lower().strip()

            if not option_name:
                raise serializers.ValidationError("Option name cannot be empty.")
            
            option = Option.objects.filter(name__iexact=option_name).first()
            if not option:
                available_options = ", ".join(
                    Option.objects.values_list('name', flat=True)
                )
                raise serializers.ValidationError(
                    f"Option '{option_name}' does not exist. Available options: {available_options}"
                )
        
        return value
            
    def create(self, validated_data):
        options_data = validated_data.pop("options", [])

        product_variant = ProductVariant.objects.create(**validated_data)

        with transaction.atomic():
            for option_data in options_data:
                option_name = option_data.get('option', '').lower().strip()
                value_name = option_data.get('value', '').lower().strip()

                option = Option.objects.get(name=option_name)


                option_value, _ = OptionValue.objects.get_or_create(
                    option=option,
                    value=value_name
                )

                ProductVariantOptionValue.objects.create(
                    product_variant=product_variant,
                    option_value=option_value
                )
        
        return product_variant 