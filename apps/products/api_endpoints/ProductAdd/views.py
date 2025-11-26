from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from .serializers import ProductCreateSerializer


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser, ]



__all__ = [
    "ProductCreateAPIView"
]
