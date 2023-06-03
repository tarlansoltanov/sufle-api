from rest_framework import serializers

from server.apps.category.models import Category


class CategoryReadSerializer(serializers.ModelSerializer):
    """Serializer for Reading Categories."""
    main_category = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        """Meta definition for CategorySerializer."""

        model = Category
        fields = '__all__'


    def get_main_category(self, obj):
        if obj.main_category:
            return {'id': obj.main_category.id, 'name': obj.main_category.name}
        return None
    
    def get_sub_categories(self, obj):
        if obj.main_category is None:
            return CategoryReadSerializer(obj.sub_categories.all(), many=True).data
        return None
