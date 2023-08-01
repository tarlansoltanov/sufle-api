from rest_framework import serializers

from server.apps.category.logic.serializers import (
    CategoryReadSerializer as CategorySerializer,
)

from ..models import Banner, Advert


class BannerSerializer(serializers.ModelSerializer):
    """Serializer definition for Banner."""

    class Meta:
        """Meta definition for BannerSerializer."""

        model = Banner
        fields = [
            "id",
            "photo",
            "deadline",
            "modified_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "modified_at",
            "created_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        data["photo"] = request.build_absolute_uri(instance.photo.url)

        return data


class AdvertReadSerializer(serializers.ModelSerializer):
    """Serializer definition for Advert."""

    class Meta:
        """Meta definition for AdvertSerializer."""

        model = Advert
        fields = [
            "id",
            "title",
            "photo",
            "category",
            "modified_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "modified_at",
            "created_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        data["photo"] = request.build_absolute_uri(instance.photo.url)
        data["category"] = CategorySerializer(
            instance.category, context=self.context
        ).data

        return data
