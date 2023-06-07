from rest_framework import serializers
from server.apps.category.logic.serializers import CategoryReadSerializer

from ..models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImage."""

    image = serializers.SerializerMethodField()

    class Meta:
        """Meta definition for ProductImageSerializer."""

        model = ProductImage
        fields = ("id", "image")

    def get_image(self, obj):
        """Get image of product."""
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)


class ProductReadSerializer(serializers.ModelSerializer):
    """Serializer for Reading Products."""

    images = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        """Meta definition for ProductSerializer."""

        model = Product
        fields = (
            "id",
            "name",
            "category",
            "images",
            "ingredients",
            "price",
            "discount",
            "is_new",
            "created_at",
        )

    def get_images(self, obj):
        """Get images of product."""
        return ProductImageSerializer(
            obj.images.all(), context=self.context, many=True
        ).data

    def get_category(self, obj):
        """Get category of product."""
        return CategoryReadSerializer(obj.category, main=True).data
