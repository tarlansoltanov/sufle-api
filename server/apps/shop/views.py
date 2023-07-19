from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Shop
from .logic.serializers import ShopReadSerializer


class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Shop."""

    model = Shop
    serializer_class = ShopReadSerializer
    queryset = Shop.objects.all().order_by("id")
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"], pagination_class=None)
    def main(self, request):
        """Return main shop."""
        queryset = Shop.objects.filter(is_main=True).first()
        serializer = ShopReadSerializer(
            queryset, many=False, context={"request": request}
        )
        return Response(serializer.data)
