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

    def validate_is_main(self, value):
        if value is True:
            main_shop = Shop.objects.filter(is_main=True).first()
            if main_shop:
                main_shop.is_main = False
                main_shop.save()

        return value
