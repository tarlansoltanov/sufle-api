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


class Advert(models.Model):
    """Model definition for Advert."""

    photo = models.ImageField(upload_to="advert/")
    title = models.CharField(max_length=255)
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Advert."""

        verbose_name = "Advert"
        verbose_name_plural = "Adverts"

    def __str__(self):
        """Unicode representation of Advert."""
        return f"{self.title} - {self.category}"
