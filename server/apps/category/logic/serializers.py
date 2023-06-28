from rest_framework import serializers

from drf_yasg.utils import swagger_serializer_method
import drf_yasg.openapi as openapi

from server.apps.category.models import Category


class CategoryLogoSerializer(serializers.ModelSerializer):
    """Serializer for Category Logo."""

    white = serializers.SerializerMethodField()
    red = serializers.SerializerMethodField()
    grey = serializers.SerializerMethodField()

    class Meta:
        """Meta definition for CategoryLogoSerializer."""

        model = Category
        fields = ("white", "red", "grey")

    def get_white(self, obj):
        return obj.logo_white.url if obj.logo_white else None

    def get_red(self, obj):
        return obj.logo_red.url if obj.logo_red else None

    def get_grey(self, obj):
        return obj.logo_grey.url if obj.logo_grey else None


class CategoryReadSerializer(serializers.ModelSerializer):
    """Serializer for Reading Categories."""

    main_category = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        """Meta definition for CategorySerializer."""

        model = Category
        fields = ("id", "name", "logo", "main_category", "sub_categories", "created_at")

    def __init__(self, *args, **kwargs):
        if kwargs.pop("main", None):
            self.fields.pop("logo")
            self.fields.pop("main_category")
            self.fields.pop("sub_categories")
        super(CategoryReadSerializer, self).__init__(*args, **kwargs)

    def get_main_category(self, obj):
        if obj.main_category:
            return CategoryReadSerializer(obj.main_category, main=True).data
        return None

    def get_sub_categories(self, obj):
        if obj.main_category is None:
            return CategoryReadSerializer(
                obj.sub_categories.all(), many=True, main=True
            ).data
        return None

    @swagger_serializer_method(serializer_or_field=CategoryLogoSerializer)
    def get_logo(self, obj):
        if obj.main_category is None:
            return CategoryLogoSerializer(obj).data
        return None
