from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from server.apps.core.logic.permissions import IsAdminOrReadOnly

from .models import Category
from .logic.filters import CategoryTypeFilter
from .logic.serializers import CategoryReadSerializer, CategoryWriteSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Category."""

    model = Category
    queryset = Category.objects.all()

    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [CategoryTypeFilter]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return CategoryWriteSerializer
        return CategoryReadSerializer

    @action(methods=["get"], detail=False)
    def main(self, request):
        serializer = self.get_serializer(
            self.queryset.prefetch_related("sub_categories").filter(main_category=None),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
