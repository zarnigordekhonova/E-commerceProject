from rest_framework import status
from rest_framework.response import Response

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.products.models import ProductVariant
from .serializers import ShoppingCartItemSerializer, AddToCartSerializer
from apps.orders.models import ShoppingCart, ShoppingCartItem


class AddToCartAPIView(CreateAPIView):
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
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product_variant_id = serializer.validated_data['product_variant_id']
        quantity = serializer.validated_data['quantity']

        try:
            product_variant = ProductVariant.objects.get(pk=product_variant_id)
        except ProductVariant.DoesNotExist:
            return Response(
                {"detail": "Product variant not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)

        try:
            cart_item = ShoppingCartItem.objects.get(cart=cart, product=product_variant)
            new_quantity = cart_item.quantity + quantity
        except ShoppingCartItem.DoesNotExist:
            new_quantity = quantity
            cart_item = None

        if product_variant.stock_quantity < new_quantity:
            return Response(
                {"detail": f"Only {product_variant.stock_quantity} items in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if cart_item:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item = cart.add_product(product_variant, quantity)

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