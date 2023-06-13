from rest_framework import viewsets, permissions

from server.apps.core.pagination import CustomPagination

from .models import Gallery
from .logic.serializers import GalleryReadSerializer


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GalleryReadSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination
