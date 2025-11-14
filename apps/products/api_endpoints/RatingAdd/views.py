from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Product
from .serializers import ProductRatingAddSerializer


class ProductRatingAddAPIView(CreateAPIView):
    """
    Generic APIView endpoint for giving a rating to product.
    POST api/products/add/rating/

    On Postman/Swagger, provide the Authorization Bearer token.

    Request body example:
    {
        "rating": 4,
        "product": 3
    }

    Response body example(201, Created):
    {
        "detail": "Rating added successfully.",
        "rating": {
            "id": 1,
            "rating": 4.0,
            "product": 3
        }
    }
    """
    serializer_class = ProductRatingAddSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        try:
            Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "detail": "Rating added successfully.",
                "rating": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    

__all__ = [
    "ProductRatingAddAPIView"
]