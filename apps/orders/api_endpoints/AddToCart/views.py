from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import ProductVariant
from .serializers import ShoppingCartItemSerializer, AddToCartSerializer
from apps.orders.models import ShoppingCartItem
from apps.orders.services import add_to_cart


class AddToCartAPIView(APIView):
    """
    Generic APIView endpoint for adding a product to the cart.

    POST api/orders/cart/add/
    On Postman/Swagger, provide the Authorization Bearer token.

    Request body example:
    {
        "product_variant_id": 2,
        "quantity": 1
    }

    Response body example(201, Created):
    {
        "detail": "Product added to cart.",
        "item": {
            "id": 1,
            "product": 2,
            "product_name": "product 1",
            "product_image": "/media/product_images/Screenshot_2025-03-26_013353.png",
            "quantity": 1,
            "subtotal": "15.00",
            "is_in_stock": true
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_variant_id = serializer.validated_data["product_variant_id"]
        quantity = serializer.validated_data["quantity"]

        try:
            product_variant = ProductVariant.objects.get(pk=product_variant_id)
        except ProductVariant.DoesNotExist:
            return Response(
                {"detail": "Product variant not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if product_variant.stock_quantity < quantity:
            return Response(
                {"detail": f"Only {product_variant.stock_quantity} items in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        add_to_cart(request.user, product_variant, quantity)

        cart_item, created = ShoppingCartItem.objects.get_or_create(
            user=request.user,
            product=product_variant,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        response_serializer = ShoppingCartItemSerializer(cart_item)
        return Response(
            {
                "detail": "Product added to cart.",
                "item": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

        

__all__ = [
    "AddToCartAPIView"
]