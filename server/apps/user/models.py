from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .logic.managers import CustomUserManager


class User(AbstractUser):
    """Custom user model."""

    username = None
    email = models.EmailField(
        _("email"), max_length=254, unique=True, null=False, blank=False
    )

    phone = models.CharField(
        _("phone"), max_length=20, unique=True, null=False, blank=False
    )
    birth_date = models.DateField(_("date of birth"), null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-id"]
