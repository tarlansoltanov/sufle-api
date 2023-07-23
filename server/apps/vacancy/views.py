from rest_framework import viewsets

from server.apps.core.logic.permissions import IsStaffOrReadOnly

from .models import Vacancy
from .logic.serializers import VacancySerializer


class VacancyViewSet(viewsets.ModelViewSet):
    """ViewSet for Vacancy."""

    model = Vacancy
    queryset = Vacancy.objects.all().prefetch_related("requirements")

    serializer_class = VacancySerializer
    permission_classes = [IsStaffOrReadOnly]
