import random

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.blog.models import Post
from apps.products.models import Product
from .serializers import ProductMinimalSerializer
from apps.blog.api_endpoints.PostList.serializers import PostListSerializer


class PostAndProductListAPIView(APIView):
    """
    APIView for getting the list of posts along with list of random products.
    GET api/blog/posts/products/list/

    Response body example(200, OK):

    {
        "posts": [
            {
            "id": 1,
            "title": "Example post",
            "short_description": "example",
            "images": [],
            "created_at": "2025-11-21 10:05:33",
            "updated_at": "2025-11-21 10:05:33"
            },
            {
            "id": 2,
            "title": "How to keep your sofa clean",
            "short_description": "Sofa cleaning",
            "images": [
                {
                "image": "/media/post_images/girly.jpg"
                }
            ],
            "created_at": "2025-11-21 10:06:00",
            "updated_at": "2025-11-21 10:15:45"
            }
        ],
        "products": [
            {
            "id": 1,
            "name": "sink",
            "designed_by": 1,
            "designed_year": 2025,
            "image": null
            },
            {
            "id": 2,
            "name": "oven",
            "designed_by": 1,
            "designed_year": 2025,
            "image": null
            }
        ]
    }
    """
    permission_classes = [AllowAny, ]

    def get(self, request):
        posts = Post.objects.prefetch_related(
            "images"
        ).order_by("id")

        all_products = list(Product.objects.prefetch_related(
            "variants__images"
        ).all())

        featured_products_count = random.randint(3, 4)
        featured_products = random.sample(
            all_products,
            min(featured_products_count, len(all_products))
        )
        
        posts_serializer = PostListSerializer(posts, many=True)
        products_serializer = ProductMinimalSerializer(featured_products, many=True)

        return Response(
            {"posts": posts_serializer.data,
             "products" : products_serializer.data},
             status=status.HTTP_200_OK
        )
    

__all__ = [
    "PostAndProductListAPIView"
]


