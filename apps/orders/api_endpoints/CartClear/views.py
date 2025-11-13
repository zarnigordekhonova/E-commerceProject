from rest_framework import status
from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import ShoppingCart


class ClearCartAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def post(self, request):
        try:
            cart = ShoppingCart.objects.get(user=request.user)
        except ShoppingCart.DoesNotExist:
            return Response(
                {"detail" : "Cart not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        cart.clear()
        return Response(
            {"detail": "Cart has been cleared."},
            status=status.HTTP_200_OK
        )


__all__ = [
    "ClearCartAPIView"
]