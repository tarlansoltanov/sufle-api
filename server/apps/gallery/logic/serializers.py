from rest_framework import serializers

from ..models import Gallery


class GalleryReadSerializer(serializers.ModelSerializer):
    """Serializer definition for Gallery."""

    url = serializers.SerializerMethodField()

    class Meta:
        """Meta definition for GallerySerializer."""

        model = Gallery
        fields = ("id", "title", "type", "url", "created_at")
        extra_kwargs = {
            "title": {"required": False},
        }

    def get_url(self, obj):
        """Return URL for the file."""
        if obj.type == "image":
            return self.context["request"].build_absolute_uri(obj.file.url)
        return obj.url
