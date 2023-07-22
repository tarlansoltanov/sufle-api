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
    CheckTokenView,
)

app_name = "users"

urlpatterns = [
    # Auth
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/register/", RegistrationView.as_view(), name="register"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/otp/send/", SendOTPView.as_view(), name="otp_send"),
    path("auth/otp/check/", CheckOTPView.as_view(), name="otp_check"),
    path("auth/reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    # Token
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/check/", CheckTokenView.as_view(), name="token_check"),
    # Account
    path("account/profile/", ProfileView.as_view(), name="profile"),
    path("account/delete/", AccountDeleteView.as_view(), name="account_delete"),
]
