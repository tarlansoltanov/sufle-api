from rest_framework import serializers

from ..models import Shop


class ShopSerializer(serializers.ModelSerializer):
    """Serializer definition for Shop model."""

    class Meta:
        """Meta definition for ShopSerializer."""

        model = Shop
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "email",
            "working_hours",
            "photo",
            "map_url",
            "is_main",
            "modified_at",
            "created_at",
        ]
        read_only_fields = ["id", "modified_at", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        data["photo"] = request.build_absolute_uri(instance.photo.url)

        return data
