from django.db import models

from server.apps.core.models import BaseModel


class Category(BaseModel):
    """Model definition for Category."""

    name = models.CharField(max_length=255)
    logo_white = models.FileField(upload_to="category/", blank=True, null=True)
    logo_red = models.FileField(upload_to="category/", blank=True, null=True)
    logo_grey = models.FileField(upload_to="category/", blank=True, null=True)
    main_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_categories",
    )

    class Meta(BaseModel.Meta):
        """Meta definition for Category."""

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """Unicode representation of Category."""

        return self.name
