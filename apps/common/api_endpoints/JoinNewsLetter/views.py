from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from .serializers import NewsLetterSerializer


class  JoinNewsLetterAPIView(CreateAPIView):
    serializer_class = NewsLetterSerializer
    permission_classes = [AllowAny, ]



__all__ = [
    "JoinNewsLetterAPIView"
]