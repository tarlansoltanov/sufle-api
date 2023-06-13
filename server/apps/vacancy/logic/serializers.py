from rest_framework import serializers

from ..models import Vacancy, Requirement


class VacancyReadSerializer(serializers.ModelSerializer):
    """Serializer for Vacancy."""

    class Meta:
        """Meta for VacancyReadSerializer."""

        model = Vacancy
        fields = "__all__"
