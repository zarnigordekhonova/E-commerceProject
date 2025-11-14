from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order, OrderDetail


class OrderCancelAPIView(APIView):
    """
    Generic APIView endpoint for cancelling the order
    POST api/orders/cancel/id/

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example:
    {
        "detail": "Order has been cancelled."
    } 
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if order.status in [Order.OrderStatus.DELIVERED, Order.OrderStatus.SHIPPING, Order.OrderStatus.REFUNDED]:
            return Response(
                {"detail": f"Cannot cancel order with status {order.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = Order.OrderStatus.CANCELED
        order.save()

        return Response(
            {"detail": "Order has been cancelled."},
            status=status.HTTP_200_OK
        )
    __all__ = [
        "OrderCancelAPIView"
    ]

