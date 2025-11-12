from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAdminUser

from apps.blog.models import Post


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAdminUser, ]
    lookup_field = "pk"
    

__all__ = [
    "PostDeleteAPIView"
]
