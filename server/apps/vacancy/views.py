from rest_framework import viewsets, permissions

from .models import Vacancy
from .logic.serializers import VacancyReadSerializer


class VacancyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Vacancy."""

    model = Vacancy
    serializer_class = VacancyReadSerializer
    queryset = Vacancy.objects.all().order_by("-created_at")
    permission_classes = [permissions.AllowAny]
