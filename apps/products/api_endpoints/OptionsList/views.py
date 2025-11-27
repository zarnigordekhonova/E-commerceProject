from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from apps.products.models import Option
from .serializers import OptionsListSerializer


class OptionsListAPIView(ListAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionsListSerializer
    permission_classes = [IsAdminUser, ]



__all__ = [
    "OptionsListAPIView"
]
