from django.db import models


class Gallery(models.Model):
    """Model definition for Gallery."""

    TYPE_CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
    )

    title = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file = models.FileField(upload_to="gallery")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Gallery."""

        verbose_name = "Gallery"
        verbose_name_plural = "Gallery Items"

    def __str__(self):
        """Unicode representation of Gallery."""
        return self.title
