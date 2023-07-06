from rest_framework import viewsets, permissions

from .models import Banner, Advert
from .logic.serializers import BannerReadSerializer, AdvertReadSerializer


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Banner."""

    model = Banner
    serializer_class = BannerReadSerializer
    queryset = Banner.objects.all().order_by("-created_at")
    permission_classes = [permissions.AllowAny]


class AdvertViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Advert."""

    model = Advert
    serializer_class = AdvertReadSerializer
    queryset = Advert.objects.all().order_by("-modified_at")
    permission_classes = [permissions.AllowAny]
