from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.products.models import Product
from .serializers import ProductListByCategorySerializer


class ProductListByCategoryAPIView(ListAPIView):
    serializer_class = ProductListByCategorySerializer
    permission_classes = [AllowAny, ]
    lookup_field = "pk"
    lookup_url_kwarg = "category_id"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        queryset = Product.objects.filter(
            category_id=category_id
        ).prefetch_related(
            "images",
            "variants"
        )
        return queryset
    

__all__ = [
    "ProductListByCategoryAPIView"
]
    