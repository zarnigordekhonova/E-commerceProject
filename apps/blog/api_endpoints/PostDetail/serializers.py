from rest_framework import serializers

from apps.blog.models import Post
from apps.blog.api_endpoints.PostList.serializers import PostImageSerializer


class PostDetailSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(source="posts", many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id", 
            "title", 
            "slug",
            "short_description",
            "description",
            "images",
            "created_at",
            "updated_at",
        )
