from rest_framework import serializers

from apps.products.models import ProductComment


class ProductCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = (
            "id",
            "comment",
            "product"
        )

    def create(self, validated_data):
        validated_data["user"] = self.context['request'].user
        return super().create(validated_data)