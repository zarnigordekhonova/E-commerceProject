from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from apps.blog.models import Post
from .serializers import PostDetailSerializer


class PostDetailAPIView(RetrieveAPIView):
    """
    Generic APIView endpoint for retrieving single post data.

    GET api/blog/post/id/detail/

    Response body example(200 OK):
    {
        "id": 1,
        "title": "Home Furniture",
        "slug": "home-furniture",
        "short_description": "home",
        "description": "home furniture stuff",
        "images": [],
        "created_at": "2025-11-14 10:53:53",
        "updated_at": "2025-11-14 10:53:53"
    }
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny, ]
    lookup_field = "pk"


__all__ = [
    "PostDetailAPIView"
]