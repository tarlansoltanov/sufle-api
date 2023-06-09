from rest_framework import serializers

from ..models import Shop


class ShopReadSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = "__all__"

    def get_photo(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.photo.url)
