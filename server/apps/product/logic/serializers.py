from rest_framework import serializers
from server.apps.category.logic.serializers import CategoryReadSerializer

from ..models import Product, ProductImage, ProductWeight


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
            "views",
            "modified_at",
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


class WeightReadSerializer(serializers.ModelSerializer):
    """Serializer for Reading ProductWeight."""

    class Meta:
        """Meta definition for WeightReadSerializer."""

        model = ProductWeight
        fields = ("id", "person_count", "weight")


class ProductWriteSerializer(serializers.ModelSerializer):
    """Serializer for Writing Products."""

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )
    old_images = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, min_length=0, required=False
    )

    class Meta:
        """Meta definition for ProductWriteSerializer."""

        model = Product
        fields = (
            "id",
            "name",
            "images",
            "uploaded_images",
            "old_images",
            "category",
            "ingredients",
            "price",
            "discount",
            "is_new",
            "views",
            "modified_at",
            "created_at",
        )
        read_only_fields = ("id", "images", "views", "created_at")

    def to_representation(self, obj):
        data = super(ProductWriteSerializer, self).to_representation(obj)
        if data.get("category"):
            data["category"] = CategoryReadSerializer(obj.category, main=True).data
        if data.get("images"):
            data["images"] = ProductImageSerializer(
                obj.images.all(), context=self.context, many=True
            ).data
        return data

    def validate(self, attrs):
        uploaded_images = attrs.get("uploaded_images", [])
        if self.instance is None and len(uploaded_images) < 2:
            raise serializers.ValidationError(
                "At least 2 images must be uploaded for a product."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        old_images = validated_data.pop("old_images", [])
        uploaded_images = validated_data.pop("uploaded_images", [])
        for image_id in old_images:
            instance.images.filter(id=image_id).delete()

        for image in uploaded_images:
            ProductImage.objects.create(product=instance, image=image)
        return super().update(instance, validated_data)
