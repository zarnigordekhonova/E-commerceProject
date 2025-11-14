from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import UserGetProfileSerializer


class UserGetUpdateProfileAPIView(RetrieveUpdateAPIView):
    """
    Generic APIView endpoint for retrieving/updating user profile.
    
    GET/PUT/PATCH  api/accounts/user/profile/

    For each method, on Postman/Swagger, provide the Authorization Bearer token.

    Response body example for GET method(200 OK):
    {
        "full_name": "Ramona Wilson",
        "username": "ramone_123",
        "email": "de19zarnigor72@gmail.com"
    }

    Request body example for PATCH method:
    {
        "username" : "ramona_wilson6"
    }

    Response body example(200 OK):
    {
        "full_name": "Ramona Wilson",
        "username": "ramona_wilson6",
        "email": "de19zarnigor72@gmail.com"
    }
    """
    serializer_class = UserGetProfileSerializer
    permission_classes = [IsAuthenticated, ]


    def get_object(self):
        return self.request.user
    

__all__ = [
    "UserGetUpdateProfileAPIView"
]


