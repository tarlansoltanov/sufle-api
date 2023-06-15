from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from server.apps.core.pagination import CustomPagination

from .models import Category
from .logic.serializers import CategoryReadSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Category."""

    model = Category
    serializer_class = CategoryReadSerializer
    queryset = (
        Category.objects.select_related("main_category")
        .prefetch_related("sub_categories")
        .all()
        .order_by("id")
    )
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    @action(methods=["get"], detail=False)
    def main(self, request):
        serializer = self.get_serializer(
            self.queryset.filter(main_category=None), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
