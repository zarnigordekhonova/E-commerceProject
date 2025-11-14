from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView

from apps.blog.models import Post
from .serializers import PostUpdateGetSerializer


class PostUpdateGetAPIView(RetrieveUpdateAPIView):
    """
    Generic APIView endpoint for updating/retrieving single post data.
    For superusers.

    GET/PUT/PATCH api/blog/post/id/update/

    On Postman/Swagger, provide the Authorization Bearer token.
    """
    queryset = Post.objects.all()
    serializer_class = PostUpdateGetSerializer
    permission_classes = [IsAdminUser, ]
    lookup_field = "pk"


__all__ = [
    "PostUpdateGetAPIView"
]


