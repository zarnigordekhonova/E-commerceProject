from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import UserDeliveryAddres


class DeliveryAddressDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserDeliveryAddres.objects.filter(user=self.request.user)
    

__all__ = [
    "DeliveryAddressDeleteAPIView"
]
    