from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=255)
    logo = models.FileField(upload_to="category/", blank=True, null=True)
    main_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_categories",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Category."""

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def clean(self):
        if self.main_category is None and not bool(self.logo):
            raise ValidationError("You can not create main category without logo")

        if self.main_category and self.main_category.main_category:
            raise ValidationError("You can not create sub category for sub category")

        if self.main_category and bool(self.logo):
            raise ValidationError("You can not create sub category with logo")
