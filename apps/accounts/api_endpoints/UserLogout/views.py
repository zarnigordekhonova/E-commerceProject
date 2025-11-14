from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class UserLogoutAPIView(APIView):
    """
    APIView endpoint for logging out.
    POST api/accounts/user/logout/

    On Postman/Swagger, provide the Authorization Bearer token.

    Request body example:
    {
        "refresh" : "your_refresh_token"
    }

    Request body example(200 OK):
    {
        "success": "Logged out successfully"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh Token is required."}
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error":"Token is expired or invalid."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Logout failed."},
                            status=status.HTTP_400_BAD_REQUEST)
        

__all__ = [
    "UserLogoutAPIView"
]
