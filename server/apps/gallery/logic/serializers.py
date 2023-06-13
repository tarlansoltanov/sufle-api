from rest_framework import serializers

from ..models import Gallery


class GalleryReadSerializer(serializers.ModelSerializer):
    """Serializer definition for Gallery."""

    class Meta:
        """Meta definition for GallerySerializer."""

        model = Gallery
        fields = "__all__"
