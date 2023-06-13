from rest_framework import serializers

from ..models import Vacancy, Requirement


class VacancyReadSerializer(serializers.ModelSerializer):
    """Serializer for Vacancy."""

    requirements = serializers.SerializerMethodField()

    class Meta:
        """Meta for VacancyReadSerializer."""

        model = Vacancy
        fields = "__all__"

    def get_requirements(self, obj):
        """Get requirements for vacancy."""
        return Requirement.objects.filter(vacancy=obj).values_list(
            "description", flat=True
        )
