from django.db import models
from django.core.exceptions import ValidationError

import logging


class Gallery(models.Model):
    """Model definition for Gallery."""

    TYPE_CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
    )

    title = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file = models.FileField(upload_to="gallery", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Gallery."""

        verbose_name = "Gallery"
        verbose_name_plural = "Gallery Items"

    def clean(self):
        if self.type == "image" and self.url:
            raise ValidationError(
                "Image type cannot have a URL. Please upload the image file."
            )

        if self.type == "video" and self.file:
            raise ValidationError(
                "Video type cannot have a file. Please provide a URL instead."
            )

        if self.type == "image" and not self.file.name:
            raise ValidationError("Image type must have a file.")

        if self.type == "video" and self.url is None:
            raise ValidationError("Video type must have a URL.")

    def __str__(self):
        """Unicode representation of Gallery."""
        return "{} - {}".format(self.title, self.type)
