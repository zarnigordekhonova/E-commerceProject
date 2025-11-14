from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import FavoriteProductCreateSerializer
from apps.products.models import ProductVariant, UserProductFavorite


# Endpoint that handles both adding and removing the product from the wishlist.
class AddToWishlistAPIView(APIView):
    """
    APIView endpoint for adding/removing product from wishlist.
    POST api/products/wishlist/id/add/

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example for adding the product(201, Created):
    {
        "detail": "Product added to favorites.",
        "favorite": {
            "id": 4,
            "product": {
                "id": 1,
                "color": "Black",
                "price": "10000.00",
                "discount_percentage": 0.0
            },
            "product_name": "product 2",
            "product_image": null,
            "created_at": "2025-11-14 08:24:45"
        }
    }

    Response body example for removing the product(200, OK):
    {
        "detail": "Product removed from favorites."
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, product_variant_id):
        try:
            product_variant = ProductVariant.objects.get(pk=product_variant_id)
        except ProductVariant.DoesNotExist:
            return Response(
                {"detail": "Product variant not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        favorite, created = UserProductFavorite.objects.get_or_create(
            user=request.user,
            product=product_variant
        )

        if created:
            serializer = FavoriteProductCreateSerializer(favorite)
            return Response(
                {"detail": "Product added to favorites.",
                 "favorite" : serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        else:
            favorite.delete()
            return Response(
                {"detail": "Product removed from favorites."},
                status=status.HTTP_200_OK
            )
        

__all__ = [
    "AddToWishlistAPIView"
]