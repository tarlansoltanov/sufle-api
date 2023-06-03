from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from server.apps.category.models import Category
from server.apps.category.logic.serializers import CategoryReadSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    model = Category
    serializer_class = CategoryReadSerializer
    queryset = Category.objects.select_related('main_category').prefetch_related('sub_categories').all()
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=False, permission_classes=[permissions.AllowAny])
    def main(self, request):
        serializer = self.get_serializer(self.queryset.filter(main_category=None), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
