from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from server.apps.core.pagination import CustomPagination

from .models import Vacancy, Requirement
from .logic.serializers import VacancyReadSerializer


class VacancyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Vacancy."""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyReadSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Get active vacancies."""
        queryset = self.get_queryset().filter(is_active=True)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
