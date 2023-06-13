from rest_framework import viewsets, permissions

from server.apps.core.pagination import CustomPagination

from .models import Vacancy, Requirement
from .logic.serializers import VacancyReadSerializer


class VacancyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Vacancy."""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyReadSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.AllowAny]
