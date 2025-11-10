from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import DeliveryAddressSerializer


class DeliveryAddressCreateAPIView(CreateAPIView):
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


