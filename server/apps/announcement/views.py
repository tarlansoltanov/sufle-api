from rest_framework import viewsets

from .models import Banner
from .logic.serializers import BannerReadSerializer


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Banner."""

    queryset = Banner.objects.all().order_by("-created_at")
    serializer_class = BannerReadSerializer
