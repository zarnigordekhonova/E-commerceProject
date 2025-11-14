from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.products.models import Product
from .serializers import ProductListByCategorySerializer


class ProductListByCategoryAPIView(ListAPIView):
    """
    Generic APIView endpoint for getting the list of products of one category.
    GET api/products/category/id/products/

    Response body example(200 OK):
    [
        {
            "id": 1,
            "name": "product 1",
            "images": [
            {
                "image": "/media/product_images/Screenshot_2025-03-26_013353.png"
            }
            ],
            "price": 15,
            "discount_percentage": 0,
            "rating": 0
        },
        {
            "id": 3,
            "name": "kitchen table",
            "images": [],
            "price": 40,
            "discount_percentage": 0,
            "rating": 0
        },
    ]
    """
    serializer_class = ProductListByCategorySerializer
    permission_classes = [AllowAny, ]
    lookup_field = "pk"
    lookup_url_kwarg = "category_id"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        queryset = Product.objects.filter(
            category_id=category_id
        ).prefetch_related(
            "variants__images",
            "variants"
        ).order_by("id")
        return queryset
    

__all__ = [
    "ProductListByCategoryAPIView"
]
    