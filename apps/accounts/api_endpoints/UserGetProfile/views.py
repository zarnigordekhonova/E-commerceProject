from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import UserGetProfileSerializer


class UserGetUpdateProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserGetProfileSerializer
    permission_classes = [IsAuthenticated, ]


    def get_object(self):
        return self.request.user
    

__all__ = [
    "UserGetUpdateProfileAPIView"
]


