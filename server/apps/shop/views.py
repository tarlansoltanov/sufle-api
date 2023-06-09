from rest_framework import viewsets, permissions

from server.apps.core.pagination import CustomPagination

from .models import Shop
from .logic.serializers import ShopReadSerializer


class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Shop."""

    queryset = Shop.objects.all()
    serializer_class = ShopReadSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination
