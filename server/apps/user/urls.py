from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginView,
    RegistrationView,
    LogoutView,
    ProfileView,
    SendOTPView,
    CheckOTPView,
    ResetPasswordView,
    AccountDeleteView,
)

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("otp/send/", SendOTPView.as_view(), name="otp_send"),
    path("otp/check/", CheckOTPView.as_view(), name="otp_check"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("delete-account/", AccountDeleteView.as_view(), name="account_delete"),
]
