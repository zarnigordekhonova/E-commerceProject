from rest_framework import serializers

from apps.products.models import ProductRating


class ProductRatingAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = (
            "id",
            "rating",
            "product"
        )

    def create(self, validated_data):
        validated_data["user"] = self.context['request'].user
        instance, created = ProductRating.objects.update_or_create(
            user=validated_data['user'],
            product=validated_data['product'],
            defaults={'rating': validated_data['rating']}
        )
        return instance