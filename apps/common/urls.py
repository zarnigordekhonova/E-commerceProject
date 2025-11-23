from django.urls import path

from apps.common.api_endpoints import JoinNewsLetterAPIView

app_name = "common"

urlpatterns = [
    path("join/newsletter/", JoinNewsLetterAPIView.as_view(), name="join-newsletter"),
]