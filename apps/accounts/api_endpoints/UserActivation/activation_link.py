from django.utils.encoding import force_str
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView

CustomUser = get_user_model()


class ActivationAPIView(APIView):
    def get(self, request, uidb64, token):
        scheme = "https" if request.is_secure() else "http"
        current_site = request.get_host()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponseRedirect(f"{scheme}://{current_site}/swagger/?activation=success")
        else:
            return HttpResponseRedirect(f"{scheme}://{current_site}/swagger/?activation=failed")
        

__all__ = [
    "ActivationAPIView"
]