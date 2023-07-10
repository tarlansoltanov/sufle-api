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
        if obj.logo_white:
            return self.context["request"].build_absolute_uri(obj.logo_white.url)
        return None

    def get_red(self, obj):
        if obj.logo_red:
            return self.context["request"].build_absolute_uri(obj.logo_red.url)
        return None

    def get_grey(self, obj):
        if obj.logo_grey:
            return self.context["request"].build_absolute_uri(obj.logo_grey.url)
        return None


class CategoryReadSerializer(serializers.ModelSerializer):
    """Serializer for Reading Categories."""

    main_category = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        """Meta definition for CategoryReadSerializer."""

        model = Category
        fields = (
            "id",
            "name",
            "logo",
            "main_category",
            "sub_categories",
            "modified_at",
            "created_at",
        )

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
            return CategoryLogoSerializer(obj, context=self.context).data
        return None


class CategoryWriteSerializer(serializers.ModelSerializer):
    """Serializer for Writing Categories."""

    isMain = serializers.BooleanField(required=True, write_only=True)
    logo_white = serializers.FileField(required=False, write_only=True)
    logo_red = serializers.FileField(required=False, write_only=True)
    logo_grey = serializers.FileField(required=False, write_only=True)
    logo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Meta definition for CategoryWriteSerializer."""

        model = Category
        fields = (
            "id",
            "name",
            "logo",
            "logo_white",
            "logo_red",
            "logo_grey",
            "main_category",
            "isMain",
            "modified_at",
            "created_at",
        )
        read_only_fields = ("id", "logo", "modified_at", "created_at")

    def validate(self, data):
        """Validate the serializer."""

        errors = {}

        if data.get("isMain"):
            if data.get("main_category"):
                errors[
                    "main_category"
                ] = "You can't set a main category to a main category"

            if not data.get("logo_white"):
                errors["logo_white"] = "This field is required."

            if not data.get("logo_red"):
                errors["logo_red"] = "This field is required."

            if not data.get("logo_grey"):
                errors["logo_grey"] = "This field is required."

        else:
            if not data.get("main_category"):
                errors["main_category"] = "This field is required."

            if data.get("main_category") and data.get("main_category").main_category:
                errors[
                    "main_category"
                ] = "You can't set a sub category to a main category."

            if data.get("logo_white"):
                errors["logo_white"] = "You can't set a logo to a sub category."

            if data.get("logo_red"):
                errors["logo_red"] = "You can't set a logo to a sub category."

            if data.get("logo_grey"):
                errors["logo_grey"] = "You can't set a logo to a sub category."

        if errors:
            raise serializers.ValidationError(errors)

        data.pop("isMain")

        return data

    @swagger_serializer_method(serializer_or_field=CategoryLogoSerializer)
    def get_logo(self, obj):
        if obj.main_category is None:
            return CategoryLogoSerializer(obj, context=self.context).data
        return None
