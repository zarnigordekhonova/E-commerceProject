from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from apps.products.models import ProductVariant
from .serializers import AddProductVariantSerializer


class AddProductVariantAPIView(CreateAPIView):
    """
    Generic APIView for adding a variant for Product.
    POST 


    Request body example:
    {
        "product": 1,
        "sku_code": 5465,
        "stock_quantity": 3,
        "price": 10000,
        "discount_percentage": 10,
        "additional_info": "additional_info",
        "options" : [
            {"option": "size", "value": "5x5"}
        ]
    }

    Response body example(201, Created):
    {
        "product": 1,
        "sku_code": "5465",
        "stock_quantity": 3,
        "price": "10000.00",
        "discount_price": "9000.00",
        "discount_percentage": 10.0,
        "additional_info": "additional_info"
    }
    """

    serializer_class = AddProductVariantSerializer
    permission_classes = [IsAdminUser, ]
    



__all__ = [
    "AddProductVariantAPIView"
]
