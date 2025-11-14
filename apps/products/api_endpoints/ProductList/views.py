from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.products.models import Product
from .serializers import ProductListSerializer


class ProductsListAPIView(ListAPIView):
    """
    Generic APIView endpoint for getting all products.
    GET  api/products/list/

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example(200 OK):
    [
        {
            "id": 1,
            "name": "product 1",
            "designed_by": 1,
            "designed_year": 2025
        },
        {
            "id": 2,
            "name": "product 2",
            "designed_by": 1,
            "designed_year": 2025
        },
        {
            "id": 3,
            "name": "kitchen table",
            "designed_by": 1,
            "designed_year": 2025
        },
        {
            "id": 4,
            "name": "Kitchen cupboard",
            "designed_by": 1,
            "designed_year": 2025
        }
    ]
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["name", "designed_by__full_name"]
    filterset_fields = {
        "rating" : ["exact", "gte", "lte"],
        "is_new" : ["exact"],
        "designed_year" : ["exact", "gte", "lte"],
        "category__id" : ["exact"]
    }
    ordering_fields = ["id", "name", "rating"]


__all__ = [
    "ProductsListAPIView"
]