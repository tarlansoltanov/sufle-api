from rest_framework import viewsets, permissions

from .models import Contact
from .logic.serializers import ContactWriteSerializer


class ContactViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactWriteSerializer
    permission_classes = [permissions.AllowAny]
