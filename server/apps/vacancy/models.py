from django.db import models

from server.apps.core.models import BaseModel


class Vacancy(BaseModel):
    """Model definition for Vacancy."""

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="vacancy")
    description = models.TextField()

    class Meta(BaseModel.Meta):
        """Meta definition for Vacancy."""

        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        """Unicode representation of Vacancy."""

        return self.name


class Requirement(BaseModel):
    """Model definition for Requirement."""

    vacancy = models.ForeignKey(
        Vacancy, on_delete=models.CASCADE, related_name="requirements"
    )
    description = models.CharField(max_length=255)

    class Meta(BaseModel.Meta):
        """Meta definition for Requirement."""

        verbose_name = "Requirement"
        verbose_name_plural = "Requirements"

    def __str__(self):
        """Unicode representation of Requirement."""

        return self.description
