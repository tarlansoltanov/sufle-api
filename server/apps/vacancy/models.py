from django.db import models


class Vacancy(models.Model):
    """Model definition for Vacancy."""

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="vacancy")
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Vacancy."""

        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        """Unicode representation of Vacancy."""
        return self.name


class Requirement(models.Model):
    """Model definition for Requirement."""

    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="requirements")
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Requirement."""

        verbose_name = "Requirement"
        verbose_name_plural = "Requirements"

    def __str__(self):
        """Unicode representation of Requirement."""
        return self.description
