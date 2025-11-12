from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView

from apps.blog.models import Post
from .serializers import PostUpdateGetSerializer


class PostUpdateGetAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateGetSerializer
    permission_classes = [IsAdminUser, ]
    lookup_field = "pk"


__all__ = [
    "PostUpdateGetAPIView"
]


