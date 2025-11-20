from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserLoginSerializer


class UserLoginAPIView(TokenObtainPairView):
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
        "refresh": "your_refresh_token",
        "access": "your_access_token",
    }
    """
    serializer_class = UserLoginSerializer

    

__all__ = [
    'UserLoginAPIView'
]