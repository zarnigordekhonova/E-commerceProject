from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from .serializers import ProductCreateSerializer


class ProductCreateAPIView(CreateAPIView):
    """
    Generic APIView for adding a product.
    POST api/products/add/

    Request body example:
    {
        "name": "kitchenware",
        "description": "kitchenware furniture",
        "is_new": true,
        "designed_by": 1,
        "category": 1,
        "show_with_posts": true
    }

    Response body example(201, Created):
    {
        "id": 1,
        "name": "kitchenware",
        "slug": "kitchenware",
        "description": "kitchenware furniture",
        "is_new": true,
        "rating": 0.0,
        "designed_year": "2025-11-26",
        "designed_by": 1,
        "category": 1,
        "show_with_posts": true
    }
    """

    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser, ]



__all__ = [
    "ProductCreateAPIView"
]
