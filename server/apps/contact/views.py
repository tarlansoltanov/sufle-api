from rest_framework import viewsets, permissions

from server.apps.core.logic.permissions import IsStaff

from .models import Contact
from .logic.serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Contact."""

    model = Contact
    queryset = Contact.objects.all()

    http_method_names = ["head", "options", "get", "post", "delete"]

    serializer_class = ContactSerializer

    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""

        if self.action == "create":
            return [permissions.AllowAny()]

        return [IsStaff()]
