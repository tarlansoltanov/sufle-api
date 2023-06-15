from rest_framework import viewsets, permissions

from .logic.serializers import ContactWriteSerializer


class ContactViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    """ViewSet definition for Contact."""

    serializer_class = ContactWriteSerializer
    permission_classes = [permissions.AllowAny]
