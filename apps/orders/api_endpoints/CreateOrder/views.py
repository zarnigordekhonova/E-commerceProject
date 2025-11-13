from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderCreateSerializer


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        order_detail = order.order_details.first()
        response_data = {
            "detail": "Order created successfully!",
            "order": {
                "order_number": order.order_number,
                "created_at": order.created_at,
                "total": order.total,
                "payment_method": order_detail.payment_method if order_detail else None,
                "shipping_type": order.shipping_type,
                "status": order.status
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    

__all__ = [
    "OrderCreateAPIView"
]