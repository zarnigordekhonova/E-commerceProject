from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import ShoppingCart
from apps.orders.api_endpoints.AddToCart.serializers import ShoppingCartSerializer


class CartDetailAPIView(RetrieveAPIView):
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
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = ShoppingCart.objects.get_or_create(user=self.request.user)
        return cart
    

__all__ = [
    "CartDetailAPIView"
]