from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import UserProductFavorite
from apps.products.api_endpoints.FavoriteProductCreate.serializers import FavoriteProductCreateSerializer


class FavoriteListAPIView(ListAPIView):
    """
    Generic APIView endpoint for getting the list wishlisted products.
    GET api/products/wishlist/

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example(200, OK):
    [
        {
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
    ]
    """
    serializer_class = FavoriteProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProductFavorite.objects.filter(
            user=self.request.user
        ).select_related(
            'product__product'
        ).prefetch_related(
            'product__images'
        ).order_by('-created_at')
    

__all__ = [
    "FavoriteListAPIView"
]