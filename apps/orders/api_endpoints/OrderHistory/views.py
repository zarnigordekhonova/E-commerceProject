from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order
from .serializers import OrderHistorySerializer


class OrderHistoryAPIView(ListAPIView):
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