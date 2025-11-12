from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import ProductVariant
from .serializers import ShoppingCartItemSerializer
from apps.orders.models import ShoppingCart, ShoppingCartItem


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_variant_id = request.data.get('product_variant_id')
        quantity = request.data.get('quantity', 1)

        try:
            product_variant = ProductVariant.objects.get(pk=product_variant_id)
        except ProductVariant.DoesNotExist:
            return Response(
                {"detail": "Product variant not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)

        # Check if product already in cart
        try:
            cart_item = ShoppingCartItem.objects.get(cart=cart, product=product_variant)
            # Product exists, increase quantity by 1
            new_quantity = cart_item.quantity + quantity
        except ShoppingCartItem.DoesNotExist:
            new_quantity = quantity
            cart_item = None

        # Check stock for the new total quantity
        if product_variant.stock_quantity < new_quantity:
            return Response(
                {"detail": f"Only {product_variant.stock_quantity} items in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add or update product in cart
        if cart_item:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item = cart.add_product(product_variant, quantity)

        serializer = ShoppingCartItemSerializer(cart_item)
        return Response(
            {
                "detail": "Product added to cart.",
                "item": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


__all__ = [
    "AddToCartAPIView"
]