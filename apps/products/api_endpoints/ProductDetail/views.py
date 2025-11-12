from django.db.models import Prefetch

from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from .serializers import ProductDetailSerializer
from apps.products.models import Product, ProductComment


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny, ]
    lookup_field = "pk"

    def get_queryset(self):
        queryset = Product.objects.prefetch_related(
            "images",
            "variants",
            Prefetch(
                "product_comment",
                queryset=ProductComment.objects.select_related("user")
            ),
            "product_rating"
            ).select_related(
                "category"
            )
        return queryset
    

__all__ = [
    "ProductDetailAPIView"
]
        

