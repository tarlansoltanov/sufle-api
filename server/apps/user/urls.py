from django.urls import path

from .views import LoginView, RegistrationView

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegistrationView.as_view(), name="register"),
]