from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from server.apps.core.logic.permissions import IsStaffOrReadOnly

from .models import Shop
from .logic.serializers import ShopSerializer


class ShopViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Shop model"""

    model = Shop
    queryset = Shop.objects.all()

    serializer_class = ShopSerializer

    permission_classes = [IsStaffOrReadOnly]

    @action(detail=False, methods=["get"], pagination_class=None)
    def main(self, request):
        """Return main shop."""
        queryset = Shop.objects.filter(is_main=True).first()
        serializer = ShopSerializer(queryset, many=False, context={"request": request})
        return Response(serializer.data)
