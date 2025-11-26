from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.blog.models import Post
from apps.products.models import Product
from .serializers import PostListSerializer
from apps.blog.api_endpoints.PostAndProductList.serializers import ProductMinimalSerializer


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
    serializer_class = PostListSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        post_serializer = self.get_serializer(posts, many=True)

        # Fixed
        products = Product.objects.filter(show_with_posts=True)
        product_serializer = ProductMinimalSerializer(products, many=True)

        response_data = {
            "posts": post_serializer.data,
            "featured_products" : product_serializer.data
        }

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )


__all__ = [
    "PostListAPIView"
]

