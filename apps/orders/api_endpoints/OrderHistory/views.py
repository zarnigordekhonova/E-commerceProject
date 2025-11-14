from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order
from .serializers import OrderHistorySerializer


class OrderHistoryAPIView(ListAPIView):
    """
    Generic APIView endpoint for getting history or orders.

    GET api/orders/history/
    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example(200 OK):
    [
        {
            "id": 8,
            "order_number": "ORD11506067",
            "total": "40.00",
            "status": "PENDING",
            "shipping_type": "PICKUP",
            "shipping_cost": "5.00",
            "created_at": "2025-11-14 10:39:37",
            "order_detail": [
                {
                    "first_name": "Zarnigor",
                    "last_name": "Dekhonova",
                    "phone_number": "+998993661603",
                    "email": "user@example.com",
                    "country": 1,
                    "city": 1,
                    "state": null,
                    "street": "Yangi hayot",
                    "zip_code": "12345",
                    "payment_method": "CREDIT_CARD"
                }
            ]
        },
        {
            "id": 6,
            "order_number": "ORD12489805",
            "total": "0.00",
            "status": "CANCELED",
            "shipping_type": "PICKUP",
            "shipping_cost": "5.00",
            "created_at": "2025-11-14 10:17:55",
            "order_detail": [
                {
                    "first_name": "Zarnigor",
                    "last_name": "Dekhonova",
                    "phone_number": "+998742876794",
                    "email": "user@example.com",
                    "country": 1,
                    "city": 1,
                    "state": null,
                    "street": "Yangi hayot",
                    "zip_code": "12345",
                    "payment_method": "CREDIT_CARD"
                }
            ]
        }
    ]
    """
    serializer_class = OrderHistorySerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "order_details"
        ).order_by("-created_at")
    

__all__ = [
    "OrderHistoryAPIView"
]