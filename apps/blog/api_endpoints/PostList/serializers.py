from rest_framework import serializers

from apps.blog.models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("image",)


class PostListSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = (
            "id",
            "title", 
            "short_description",
            "images", # post related images
            "created_at",
            "updated_at",
        )
