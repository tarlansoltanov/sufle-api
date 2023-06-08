from rest_framework import serializers

from server.apps.category.models import Category


class CategoryReadSerializer(serializers.ModelSerializer):
    """Serializer for Reading Categories."""

    main_category = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()

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
