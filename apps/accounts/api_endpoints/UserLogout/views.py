from rest_framework_simplejwt.views import TokenBlacklistView


class UserLogoutAPIView(TokenBlacklistView):
    """
    APIView endpoint for logging out.
    POST api/accounts/user/logout/

    On Postman/Swagger, provide the Authorization Bearer token.

    Request body example:
    {
        "refresh" : "your_refresh_token"
    }

    Response: 204 No Content
    """
    pass
        

__all__ = [
    "UserLogoutAPIView"
]
