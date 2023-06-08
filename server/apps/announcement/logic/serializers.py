from rest_framework import serializers

from ..models import Banner


class BannerReadSerializer(serializers.ModelSerializer):
    """Serializer definition for Banner."""

    photo = serializers.SerializerMethodField()

    class Meta:
        """Meta definition for BannerSerializer."""

        model = Banner
        fields = "__all__"

    def get_photo(self, obj):
        """Return photo url."""
        request = self.context.get("request")
        photo_url = obj.photo.url
        return request.build_absolute_uri(photo_url)
