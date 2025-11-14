from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

CustomUser = get_user_model()


class ActivationAPIView(APIView):
    """
    APIView endpoint for activating user account by activation link.
    
    GET api/accounts/activate/
    
    On Swagger, for uidb64 enter two-letter encoded string,
    for token enter string that comes after the uidb64.

    Request body example:
    Activation link => http://127.0.0.1:8000/api/users/activate/Ng/cz7b3y-40dd75f16f5f435cd043d0060c8fcad9/
   
    uidb64 = Ng
    token = cz7b3y-40dd75f16f5f435cd043d0060c8fcad9

    Response body example(200 OK):
    {
        "detail": "Account has been activated successfully!"
    }    
    """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response(
                {"detail": "Invalid activation link."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {"detail": "Account has been activated successfully!"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Activation link is expired or invali."},
                status=status.HTTP_400_BAD_REQUEST
            )
        

__all__ = [
    "ActivationAPIView"
]