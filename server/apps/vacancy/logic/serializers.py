from rest_framework import serializers

from ..models import Vacancy, Requirement


class VacancySerializer(serializers.ModelSerializer):
    """Serializer for Vacancy."""

    requirements = serializers.ListField(
        child=serializers.CharField(max_length=255), write_only=True
    )

    class Meta:
        """Meta for VacancySerializer."""

        model = Vacancy
        fields = [
            "id",
            "name",
            "title",
            "photo",
            "requirements",
            "description",
            "modified_at",
            "created_at",
        ]
        read_only_fields = ["id", "modified_at", "created_at"]

    def to_representation(self, instance):
        """Override to_representation method."""

        data = super().to_representation(instance)

        data["requirements"] = instance.requirements.values_list(
            "description", flat=True
        )

        return data

    def create(self, validated_data):
        """Create vacancy."""

        requirements = validated_data.pop("requirements", [])

        vacancy = Vacancy.objects.create(**validated_data)

        for requirement in requirements:
            Requirement.objects.create(description=requirement, vacancy=vacancy)

        return vacancy

    def update(self, instance, validated_data):
        """Update vacancy."""

        requirements = validated_data.pop("requirements", [])

        instance = super().update(instance, validated_data)

        for requirement in instance.requirements.all():
            requirement.delete()

        for requirement in requirements:
            Requirement.objects.create(description=requirement, vacancy=instance)

        return instance
