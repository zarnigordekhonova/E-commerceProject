from django.db.models import Prefetch

from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from .serializers import ProductDetailSerializer
from apps.products.models import Product, ProductComment, ProductVariant


class ProductDetailAPIView(RetrieveAPIView):
    """
    Generic APIView endpoint for retrieving a single product.
    GET api/products/id/detail/

    Response body example(200 OK):
    {
        "id": 1,
        "reviews_number": 0,
        "name": "kitchenware",
        "description": "kitchenware furniture",
        "rating": 0,
        "is_new": true,
        "category": {
            "id": 1,
            "category_name": "Kitchen furniture"
        },
        "variants": [
            {
            "id": 8,
            "sku_code": "342",
            "price": "10000.00",
            "discount_price": "9000.00",
            "discount_percentage": 10,
            "stock_quantity": 3,
            "additional_info": "additional_info",
            "options": [
                {
                "option": "size",
                "value": "5x5"
                }
            ],
            "images": []
            },
            {
            "id": 9,
            "sku_code": "5465",
            "price": "10000.00",
            "discount_price": "9000.00",
            "discount_percentage": 10,
            "stock_quantity": 3,
            "additional_info": "additional_info",
            "options": [
                {
                "option": "color",
                "value": "sky blue"
                }
            ],
            "images": []
            }
        ]
    }
    """
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny, ]
    lookup_field = "pk"

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.prefetch_related(
                    "images",
                    "variant_options",
                )
            ),
            "product_rating"
        ).select_related("category")

    

__all__ = [
    "ProductDetailAPIView"
]