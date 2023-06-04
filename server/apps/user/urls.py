from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, RegistrationView, LogoutView

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegistrationView.as_view(), name="register"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
