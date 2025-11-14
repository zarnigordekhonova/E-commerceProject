from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderCreateSerializer


class OrderCreateAPIView(CreateAPIView):
    """
    Generic APIView endpoint for creating an order.

    POST api/orders/create/
    On Postman/Swagger, provide the Authorization Bearer token.

    Request body example:
    {
        "shipping_type": "PICKUP",
        "order_detail": {
                "first_name": "Zarnigor",
                "last_name": "Dekhonova",
                "phone_number": "+998742876794",
                "email": "user@example.com",
                "country": 1,
                "city": 1,
                "street": "Yangi hayot",
                "zip_code": "12345",
                "payment_method": "CREDIT_CARD"
            }
    }

    Response body example(201 Created):
    {
        "detail": "Order created successfully!",
        "order": {
            "order_number": "ORD12489805",
            "created_at": "2025-11-14T05:17:55.962395Z",
            "total": 10040.0,
            "payment_method": "CREDIT_CARD",
            "shipping_type": "PICKUP",
            "status": "PENDING"
        }
    }
    """
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

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