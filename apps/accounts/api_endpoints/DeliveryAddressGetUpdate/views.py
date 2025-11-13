from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from apps.accounts.models import UserDeliveryAddres
from apps.accounts.api_endpoints.DeliveryAddressCreate.serializers import DeliveryAddressSerializer


class DeliveryAddressUpdateGetAPIView(RetrieveUpdateAPIView):
    """
    Generic APIView for retrieving/updating user's delivery address.
    GET/PUT/PATCH api/accounts/delivery-address/id/update/

    On Postman/Swagger, provide the Authorization Bearer token.

    Response body example for GET method(200 OK):
    {
        "country": 1,
        "city": 1,
        "street": "Bunyodkor",
        "building_number": "4",
        "is_default": true
    }

    Request body example for PUT method:
    {
        "country": 1,
        "city": 1,
        "street": "Chilonzor",
        "building_number": "6A",
        "is_default": false
    }

    Response body example(200 OK):
    {
        "country": 1,
        "city": 1,
        "street": "Chilonzor",
        "building_number": "6A",
        "is_default": false
    }
    """
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserDeliveryAddres.objects.filter(user=self.request.user)
    

__all__ = [
    "DeliveryAddressUpdateGetAPIView"
]
