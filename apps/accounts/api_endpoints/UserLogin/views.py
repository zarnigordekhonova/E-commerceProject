from django.contrib.auth import login

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserLoginSerializer, UserSerializer


class UserLoginAPIView(GenericAPIView):
    """
    Generic APIView endpoint for logging in as an authenticated user.
    POST api/accounts/user/login/

    Request body example:
    {
        "email" : "your_email@example.com",
        "password": "your_password"
    }

    Response body example(200 OK):
    {
        "user": {
            "username": "your_username"
        },
        "refresh": "your_refresh_token",
        "access": "your_access_token",
        "message": "Login successful"
    }
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    

__all__ = [
    'UserLoginAPIView'
]