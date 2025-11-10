from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.blog.models import Post
from .serializers import PostListSerializer


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    authentication_classes = [AllowAny, ]


__all__ = [
    "PostListAPIView"
]

