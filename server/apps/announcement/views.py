from rest_framework import viewsets, permissions

from .models import Banner
from .logic.serializers import BannerReadSerializer


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Banner."""

    model = Banner
    serializer_class = BannerReadSerializer
    queryset = Banner.objects.all().order_by("-created_at")
    permission_classes = [permissions.AllowAny]
