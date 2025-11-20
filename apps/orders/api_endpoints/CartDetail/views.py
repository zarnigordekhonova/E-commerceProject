from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.orders.models import ShoppingCartItem
from apps.orders.api_endpoints.AddToCart.serializers import ShoppingCartItemSerializer


class CartDetailAPIView(APIView):
    """
    Generic APIView endpoint for getting cart data.
    GET api/orders/cart/detail/

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example(200 OK):
    {
        "id": 1,
        "items": [
            {
                "id": 2,
                "product": 4,
                "product_name": "kitchen table",
                "product_image": null,
                "quantity": 1,
                "subtotal": "40.00",
                "is_in_stock": true
            },
            {
                "id": 1,
                "product": 2,
                "product_name": "product 1",
                "product_image": "/media/product_images/Screenshot_2025-03-26_013353.png",
                "quantity": 1,
                "subtotal": "15.00",
                "is_in_stock": true
            }
        ],
        "total_price": "55.00",
        "is_empty": false
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = ShoppingCartItem.objects.filter(user=request.user)

        if not cart_items:
            return Response(
                {"items": [],
                 "total_price": "0.00",
                 "item_count": 0},
                status=status.HTTP_200_OK
            )
        
        serializer = ShoppingCartItemSerializer(cart_items, many=True)
        total_price = sum(item.subtotal for item in cart_items)

        return Response(
            {
                "items": serializer.data,
                "total_price": str(total_price),
                "item_count": cart_items.count()
            },
            status=status.HTTP_200_OK
        )
    

__all__ = [
    "CartDetailAPIView"
]