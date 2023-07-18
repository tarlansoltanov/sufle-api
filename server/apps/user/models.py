import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken

from .logic.managers import CustomUserManager


class User(AbstractUser):
    """Custom user model."""

    username = None
    email = models.EmailField(
        _("email"), max_length=254, unique=True, null=False, blank=False
    )

    phone = models.CharField(
        _("phone"), max_length=20, unique=True, null=True, blank=True
    )
    birth_date = models.DateField(_("date of birth"), null=True, blank=True)

    otp = models.CharField(_("otp"), max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(_("otp created at"), null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-id"]

    def generate_otp(self):
        self.otp = random.randint(100000, 999999)
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp

    def verify_otp(self, otp):
        return self.otp == otp if self.is_otp_valid() else False

    def is_otp_valid(self):
        return timezone.now() <= timezone.timedelta(minutes=5) + self.otp_created_at

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
