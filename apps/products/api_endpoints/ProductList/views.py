from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.products.models import Product
from .serializers import ProductListSerializer


class ProductsListAPIView(ListAPIView):
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