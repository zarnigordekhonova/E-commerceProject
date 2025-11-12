from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from apps.blog.models import Post
from .serializers import PostDetailSerializer


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny, ]
    lookup_field = "pk"


__all__ = [
    "PostDetailAPIView"
]