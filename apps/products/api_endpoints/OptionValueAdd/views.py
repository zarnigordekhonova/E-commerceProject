from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from .serializers import AddOptionValueSerializer


class AddOptionValueAPIView(CreateAPIView):
    """
    Generic APIView for adding a value to the option.
    POST api/products/option/value/add/

    For admin users only.

    Request body example:
    {
        "option": "color", => value is entered with the name, not ID
        "value": "sky blue"
    }

    Response body example(201, Created):
    {
        "id": 1,
        "value": "sky blue"
    }
    """
    serializer_class = AddOptionValueSerializer
    permission_classes = [IsAdminUser,]



__all__ = [
    "AddOptionValueAPIView"
]