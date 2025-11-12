from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import ShoppingCart
from apps.orders.api_endpoints.AddToCart.serializers import ShoppingCartSerializer


class CartDetailAPIView(RetrieveAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = ShoppingCart.objects.get_or_create(user=self.request.user)
        return cart
    

__all__ = [
    "CartDetailAPIView"
]