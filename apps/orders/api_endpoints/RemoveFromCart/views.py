from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import ShoppingCartItem
from apps.orders.api_endpoints.AddToCart.serializers import ShoppingCartItemSerializer


class RemoveFromCartAPIView(APIView):
    """
    Generic APIView endpoint for removing a product from cart.

    DELETE api/orders/remove/1/cart/
    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example(200 OK):
    {
        "detail": "Item removed from cart."
    }
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart_item = ShoppingCartItem.objects.get(pk=item_id, user=request.user)
        except ShoppingCartItem.DoesNotExist:
            return Response(
                {"detail": "Item not found in the cart."},
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