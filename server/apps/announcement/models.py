from django.db import models


class Banner(models.Model):
    """Model definition for Banner."""

    photo = models.ImageField(upload_to="banner/")
    deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Banner."""

        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        """Unicode representation of Banner."""
        return f"{self.photo} - {self.deadline}"
