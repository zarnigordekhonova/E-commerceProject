from rest_framework import serializers

from apps.products.models import ProductComment, ProductRating


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