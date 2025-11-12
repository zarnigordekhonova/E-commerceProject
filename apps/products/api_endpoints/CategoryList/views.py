from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.products.models import Category
from .serializers import CategorySerializer


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["category_name"]
    filterset_fields = {
        "id" : ["exact", "gt", "lt", "in"],
        "category_name" : ["exact", "icontains", "istartswith"],
        "slug" : ["exact", "icontains", "istartswith"],
    }
    ordering_fields = ["id", "category_name"]

    def get_object(self):
        categories = Category.objects.all().annotate(
            product_count = Count("products")
        )
        return categories
    

__all__ = [
    "CategoryListAPIView"
]