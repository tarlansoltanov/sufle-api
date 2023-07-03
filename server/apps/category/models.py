from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
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
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Category."""

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def clean(self):
        if self.main_category is None and (
            not bool(self.logo_grey)
            or not bool(self.logo_red)
            or not bool(self.logo_white)
        ):
            raise ValidationError(
                "You can not create main category without all the logos"
            )

        if self.main_category and self.main_category.main_category:
            raise ValidationError("You can not create sub category for sub category")

        if self.main_category and (
            bool(self.logo_grey) or bool(self.logo_red) or bool(self.logo_white)
        ):
            raise ValidationError("You can not create sub category with any logo")
