from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from server.apps.core.logic.permissions import IsAdminOrReadOnly

from .models import Gallery
from .logic.serializers import GallerySerializer


class GalleryViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Gallery."""

    model = Gallery
    queryset = Gallery.objects.all().order_by("-modified_at")

    serializer_class = GallerySerializer

    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = ["type"]
