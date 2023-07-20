from django.db import models

from server.apps.core.models import BaseModel


class Shop(BaseModel):
    """Model definition for Shop."""

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    working_hours = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="shop")
    map_url = models.URLField(max_length=255)
    is_main = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        """Meta definition for Shop."""

        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self):
        """Unicode representation of Shop."""

        return self.name
