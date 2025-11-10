from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from apps.accounts.models import UserDeliveryAddres
from apps.accounts.api_endpoints.DeliveryAddressCreate.serializers import DeliveryAddressSerializer


class DeliveryAddressUpdateGetAPIView(RetrieveUpdateAPIView):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserDeliveryAddres.objects.filter(user=self.request.user)
    

__all__ = [
    "DeliveryAddressUpdateGetAPIView"
]
