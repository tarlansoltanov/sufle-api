from django.db import models

from server.apps.core.models import BaseModel


class Contact(BaseModel):
    """Model definition for Contact."""

    TYPES_CHOICES = (
        (0, "Şikayət"),
        (1, "Təklif"),
        (2, "Vakansiya"),
    )

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(choices=TYPES_CHOICES, default=1)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        """Meta definition for Contact."""

        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        """Unicode representation of Contact."""

        return f"{self.name} {self.surname}"
