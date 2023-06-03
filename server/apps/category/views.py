from django.shortcuts import render

from rest_framework import viewsets, permissions

from server.apps.category.models import Category
from server.apps.category.logic.serializers import CategoryReadSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    model = Category
    serializer_class = CategoryReadSerializer
    queryset = Category.objects.select_related('main_category').all()
    permission_classes = [permissions.AllowAny]
