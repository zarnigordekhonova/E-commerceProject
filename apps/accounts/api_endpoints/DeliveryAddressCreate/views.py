from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import DeliveryAddressSerializer


class DeliveryAddressCreateAPIView(CreateAPIView):
    """
    Generic APIView endpoint for adding user's delivery address.
    
    POST api/accounts/delivery-address/create/

    On Postman/Swagger, provide the Authorization Bearer token.

    Request body example:
    {
        "country" : 1, => ForeignKey relation with Country model
        "city" : 1, => ForeignKey relation with City model
        "street" : "street_name",
        "building_number" : bulding_number, => can either be number or mix of numbers and ltters
        "is_default": "True/False"
    }

    Response code: 201, Created
    """
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    # Fixed, using perform_create method instead of create method
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


__all__ = [
    "DeliveryAddressCreateAPIView"
]


