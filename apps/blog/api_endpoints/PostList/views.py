from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.blog.models import Post
from .serializers import PostListSerializer


class PostListAPIView(ListAPIView):
    """
    Generic APIView endpoint for getting the list of all posts.

    GET api/blog/post/list/

    Response body example(200 OK):
    [
        {
            "id": 2,
            "title": "Examplary post",
            "short_description": "example",
            "images": [],
            "created_at": "2025-11-14 11:00:07",
            "updated_at": "2025-11-14 11:00:07"
        },
        {
            "id": 1,
            "title": "Home Furniture",
            "short_description": "home",
            "images": [],
            "created_at": "2025-11-14 10:53:53",
            "updated_at": "2025-11-14 10:53:53"
        }
    ]

    """
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny, ]


__all__ = [
    "PostListAPIView"
]

