from django.db.models import Prefetch

from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from .serializers import ProductDetailSerializer
from apps.products.models import Product, ProductComment


class ProductDetailAPIView(RetrieveAPIView):
    """
    Generic APIView endpoint for retrieving a single product.
    GET api/products/id/detail/

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example(200 OK):
    {
    "id": 3,
    "images": [],
    "reviews_number": 1,
    "name": "kitchen table",
    "description": "description",
    "rating": 0,
    "is_new": true,
    "category": "Kitchen furniture",
    "variants": [
        {
        "id": 4,
        "color": "yellow",
        "additional_info": "",
        "measurement": "4x4",
        "sku_code": "098765",
        "price": "40.00",
        "discount_price": "0.00",
        "discount_percentage": 0
        }
    ],
    "reviews": [
        {
        "id": 1,
        "user": "Ramona Wilson",
        "comment": "I like this product.",
        "rating": null,
        "created_at": "2025-11-14 05:30:57"
        }
    ]
    """
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny, ]
    lookup_field = "pk"

    def get_queryset(self):
        queryset = Product.objects.prefetch_related(
            "variants__images",
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
        

