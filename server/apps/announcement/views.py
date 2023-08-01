from rest_framework import viewsets

from server.apps.core.logic.permissions import IsStaffOrReadOnly

from .models import Banner, Advert
from .logic.serializers import BannerSerializer, AdvertReadSerializer


class BannerViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Banner."""

    model = Banner
    queryset = Banner.objects.all()

    serializer_class = BannerSerializer

    permission_classes = [IsStaffOrReadOnly]


class AdvertViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Advert."""

    model = Advert
    queryset = Advert.objects.all()

    http_method_names = ["head", "options", "get", "put", "patch"]

    serializer_class = AdvertReadSerializer

    permission_classes = [IsStaffOrReadOnly]
