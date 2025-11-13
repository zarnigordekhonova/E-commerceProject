from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import UserDeliveryAddres


class DeliveryAddressDeleteAPIView(DestroyAPIView):
    """
    Generic APIView for deleting user's delivery address.
    DELETE api/accounts/delivery-address/id/delete/

    On Postman/Swagger, provide the Authorization Bearer token.
    Response body returns just status code, 204 No Content.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserDeliveryAddres.objects.filter(user=self.request.user)
    

__all__ = [
    "DeliveryAddressDeleteAPIView"
]
    