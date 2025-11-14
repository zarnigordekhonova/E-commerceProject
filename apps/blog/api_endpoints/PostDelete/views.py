from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAdminUser

from apps.blog.models import Post


class PostDeleteAPIView(DestroyAPIView):
    """
    Generic APIView endpoint for deleting post data.
    For superusers.

    DELETE api/blog/post/id/delete/

    On Postman/Swagger, provide the Authorization Bearer token.
    """
    queryset = Post.objects.all()
    permission_classes = [IsAdminUser, ]
    lookup_field = "pk"
    

__all__ = [
    "PostDeleteAPIView"
]
