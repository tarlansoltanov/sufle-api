from rest_framework import serializers

from ..models import Gallery


class GallerySerializer(serializers.ModelSerializer):
    """Serializer definition for Gallery."""

    class Meta:
        """Meta definition for GallerySerializer."""

        model = Gallery
        fields = ("id", "title", "type", "file", "url", "modified_at", "created_at")

        read_only_fields = ("id", "created_at")

        extra_kwargs = {
            "file": {"write_only": True},
        }

    def to_representation(self, instance):
        """Override to_representation method."""

        data = super(GallerySerializer, self).to_representation(instance)
        request = self.context.get("request")

        if data["type"] == "image":
            data["url"] = request.build_absolute_uri(instance.file.url)

        return data

    def validate(self, attrs):
        """Override validate method."""

        errors = {}

        if attrs["type"] == "image":
            if not attrs.get("file"):
                if not self.instance or not self.instance.file.name:
                    errors["file"] = "This field is required."

            if attrs.get("url"):
                errors["url"] = "This field should not be provided for image type."

        elif attrs["type"] == "video":
            if not attrs.get("url"):
                if not self.instance or not self.instance.url:
                    errors["url"] = "This field is required."

            if attrs.get("file"):
                errors["file"] = "This field should not be provided for video type."

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(attrs)
