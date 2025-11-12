from django.urls import path

from .api_endpoints import (
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserGetUpdateProfileAPIView,
    ActivationAPIView,

    DeliveryAddressCreateAPIView,
    DeliveryAddressUpdateGetAPIView,
    DeliveryAddressDeleteAPIView,
)

app_name = "accounts"

urlpatterns = [
    path("user/register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("user/login/", UserLoginAPIView.as_view(), name="user-login"),
    path("user/profile/", UserGetUpdateProfileAPIView.as_view(), name="user-profile"),
    path("user/logout/", UserLogoutAPIView.as_view(), name="user-logout"),
    path("activate/<uidb64>/<token>/", ActivationAPIView.as_view(), name="activate"),

    path("delivery-address/create/", DeliveryAddressCreateAPIView.as_view(), name="delivery-address-create"),
    path("delivery-address/<int:pk>/update/", DeliveryAddressUpdateGetAPIView.as_view(), name="delivery-address-update"),
    path("delivery-address/<int:pk>/delete/", DeliveryAddressDeleteAPIView.as_view(), name="delivery-address-delete"),
]