from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from server.apps.core.pagination import CustomPagination

from .models import Product, ProductWeight
from .logic.serializers import ProductReadSerializer, WeightReadSerializer
from .logic.filters import PriceAndDiscountRangeFilter, CategoryFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for Product."""

    model = Product
    serializer_class = ProductReadSerializer
    queryset = (
        Product.objects.select_related("category")
        .prefetch_related("images")
        .all()
        .order_by("id")
    )
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        PriceAndDiscountRangeFilter,
        CategoryFilter,
    ]

    filterset_fields = ["is_new"]
    search_fields = ["name", "category__name"]
    ordering_fields = ["price", "created_at"]


class WeightViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for ProductWeight."""

    model = ProductWeight
    serializer_class = WeightReadSerializer
    queryset = ProductWeight.objects.all().order_by("person_count")
    permission_classes = [permissions.AllowAny]
