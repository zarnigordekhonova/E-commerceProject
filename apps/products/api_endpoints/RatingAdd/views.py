from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Product
from .serializers import ProductRatingAddSerializer


class ProductRatingAddAPIView(CreateAPIView):
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