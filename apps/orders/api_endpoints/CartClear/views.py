from django.core.cache import cache

from rest_framework import status
from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import ShoppingCartItem


class ClearCartAPIView(APIView):
    """
    APIView endpoint for clearing the cart.
    POST api/orders/clear/cart/

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example(200 OK):
    {
        "detail": "Cart has been cleared."
    }
    """
    permission_classes = [IsAuthenticated, ]
    
    def post(self, request):
        ShoppingCartItem.objects.filter(user=request.user).delete()

        cache_key = f"cart_{request.user.id}"
        cache.delete(cache_key)

        return Response(
            {"detail": "Cart has been cleared"},
            status=status.HTTP_200_OK
        )


__all__ = [
    "ClearCartAPIView"
]