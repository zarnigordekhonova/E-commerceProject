from rest_framework import serializers

from apps.blog.models import Post


class PostUpdateGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "short_description",
            "created_at",
            "updated_at"
        )
        read_only_fields = ["id", "created_at", "updated_at"] 