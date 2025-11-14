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

    Response body example(201 Created):
    {
        "detail": "Delivery address has been added successfully."
    }
    """
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(
            {"detail" : "Delivery address has been added successfully."},
            status=status.HTTP_201_CREATED
        )


__all__ = [
    "DeliveryAddressCreateAPIView"
]


