from django.db import models

from server.apps.core.models import BaseModel


class Gallery(BaseModel):
    """Model definition for Gallery."""

    TYPE_CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
    )

    title = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file = models.FileField(upload_to="gallery", blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        """Meta definition for Gallery."""

        verbose_name = "Gallery"
        verbose_name_plural = "Gallery Items"

    def __str__(self):
        """Unicode representation of Gallery."""

        return "{} - {}".format(self.title, self.type)
