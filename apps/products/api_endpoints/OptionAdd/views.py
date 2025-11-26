from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from .serializers import OptionCreateSerializer


class OptionCreateAPIView(CreateAPIView):
    """
    Generic APIView for adding product option.
    POST api/products/option/add/

    For admin users only.
    
    Request body example:
    {
        "name" : "color"
    }

    Response body example(201, Created):
    {
        "id": 1,
        "name": "color"
    }
    """

    serializer_class = OptionCreateSerializer
    permission_classes = [IsAdminUser, ]



__all__ = [
    "OptionCreateAPIView"
]
