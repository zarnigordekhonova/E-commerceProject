from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.products.models import Category
from .serializers import CategorySerializer


class CategoryListAPIView(ListAPIView):
    """
    Generic APIView for getting the list of available categories.
    GET api/products/categories/

    Response body example(200 OK):
    [
         {
            "id": 1,
            "category_name": "Kitchen furniture",
            "slug": "kitchen-furniture",
            "product_count": 0,
            "created_at": "2025-11-13 11:26:05",
            "updated_at": "2025-11-13 11:26:05"
        },
        {
            "id": 2,
            "category_name": "Tables",
            "slug": "tables",
            "product_count": 0,
            "created_at": "2025-11-13 11:26:32",
            "updated_at": "2025-11-13 11:26:32"
        },
    ]
    """
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["category_name"]
    filterset_fields = {
        "id" : ["exact", "gt", "lt", "in"],
        "category_name" : ["exact", "icontains", "istartswith"],
        "slug" : ["exact", "icontains", "istartswith"],
    }
    ordering_fields = ["id"]

    def get_queryset(self):
        categories = Category.objects.all().annotate(
            product_count = Count("products")
        )
        return categories
    

__all__ = [
    "CategoryListAPIView"
]