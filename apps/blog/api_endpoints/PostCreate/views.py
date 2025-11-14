from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from apps.blog.models import Post
from .serializers import PostSerializer


class PostCreateAPIView(CreateAPIView):
    """
    Generic APIView endpoint for adding a post.

    POST api/blog/post/create/

    On Postman/Swagger, provide the Authorization Bearer token.

    Request body example:
    {
        "title": "Home Furniture",
        "short_description": "home",
        "description": "home furniture stuff"
    }

    Response body example(201 Created):
    {
        "title": "Home Furniture",
        "short_description": "home",
        "description": "home furniture stuff"
    }
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminUser]


__all__ = [
    "PostCreateAPIView"
]