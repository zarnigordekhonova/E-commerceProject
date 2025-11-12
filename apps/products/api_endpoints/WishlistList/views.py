from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import UserProductFavorite
from apps.products.api_endpoints.FavoriteProductCreate.serializers import FavoriteProductCreateSerializer


class FavoriteListAPIView(ListAPIView):
    serializer_class = FavoriteProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProductFavorite.objects.filter(
            user=self.request.user
        ).select_related(
            'product__product'
        ).prefetch_related(
            'product__product__images'
        ).order_by('-created_at')
    

__all__ = [
    "FavoriteListAPIView"
]