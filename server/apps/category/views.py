from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Category
from .logic.serializers import CategoryReadSerializer, CategoryWriteSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Category."""

    model = Category

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return CategoryWriteSerializer
        return CategoryReadSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        if self.action in ["create", "update", "partial_update", "destroy", "retrieve"]:
            return Category.objects.all()
        return (
            Category.objects.select_related("main_category")
            .prefetch_related("sub_categories")
            .all()
            .order_by("-modified_at")
        )

    @action(methods=["get"], detail=False)
    def main(self, request):
        serializer = self.get_serializer(
            self.queryset.filter(main_category=None), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
