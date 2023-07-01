from rest_framework import viewsets, permissions

from .models import Gallery
from .logic.serializers import GalleryReadSerializer


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Gallery."""

    model = Gallery
    serializer_class = GalleryReadSerializer
    queryset = Gallery.objects.all().order_by("-created_at")
    permission_classes = [permissions.AllowAny]
