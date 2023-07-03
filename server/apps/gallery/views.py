from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Gallery
from .logic.serializers import GalleryReadSerializer


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Gallery."""

    model = Gallery
    serializer_class = GalleryReadSerializer
    queryset = Gallery.objects.all().order_by("-created_at")
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        DjangoFilterBackend,
    ]

    filterset_fields = ["type"]
