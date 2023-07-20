from django.db import models


class BaseModel(models.Model):
    """BaseModel definition."""

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for BaseModel."""

        abstract = True
        ordering = ["-modified_at"]
