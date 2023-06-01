from django.db import models


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=255)
    logo = models.FileField(upload_to='category/')
    main_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_categories'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name
