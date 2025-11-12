from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import ShoppingCart, ShoppingCartItem
from apps.orders.api_endpoints.AddToCart.serializers import ShoppingCartItemSerializer


class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart = ShoppingCart.objects.get(user=request.user)
        except ShoppingCart.DoesNotExist:
            return Response(
                {"detail": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            cart_item = ShoppingCartItem.objects.get(pk=item_id, cart=cart)
        except ShoppingCartItem.DoesNotExist:
            return Response(
                {"detail": "Item not found in cart."},
                status=status.HTTP_404_NOT_FOUND
            )

        if cart_item.quantity == 1:
            cart_item.delete()
            return Response(
                {"detail": "Item removed from cart."},
                status=status.HTTP_200_OK
            )
        else:
            # Decrease quantity by 1
            cart_item.quantity -= 1
            cart_item.save()
            serializer = ShoppingCartItemSerializer(cart_item)
            return Response(
                {
                    "item": serializer.data
                },
                status=status.HTTP_200_OK
            )
        

__all__ = [
    "RemoveFromCartAPIView"
]