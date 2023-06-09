from django.db import models


class Shop(models.Model):
    """Model definition for Shop."""

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    working_hours = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="shop")
    map_url = models.URLField(max_length=255)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Shop."""

        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self):
        """Unicode representation of Shop."""
        return self.name
