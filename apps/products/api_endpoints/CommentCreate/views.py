from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Product
from .serializers import ProductCommentCreateSerializer


class ProductCommentCreateAPIView(CreateAPIView):
    """
    Generic APIView endpoint for commenting on a specific product.
    POST api/products/comment/create/

    On Postman/Swagger, provide the Authorization Bearer token.

    Request body example:
    {
        "comment": "I like this product.",
        "product": 3
    }

    Response body example(201 Created):
    {
        "detail": "Comment created successfully.",
        "comment": {
            "id": 1,
            "comment": "I like this product.",
            "product": 3
        }
    }
    """
    serializer_class = ProductCommentCreateSerializer
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
                "detail": "Comment created successfully.",
                "comment": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


    

__all__ = [
    "ProductCommentCreateAPIView"
]