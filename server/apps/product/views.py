from rest_framework.response import Response
from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from server.apps.core.logic.pagination import CustomPagination
from server.apps.core.logic.permissions import IsStaffOrReadOnly

from .models import Product, ProductWeight
from .logic.serializers import (
    ProductReadSerializer,
    ProductWriteSerializer,
    WeightSerializer,
)
from .logic.filters import PriceAndDiscountRangeFilter, CategoryFilter


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Product."""

    model = Product
    queryset = (
        Product.objects.select_related("category").prefetch_related("images").all()
    )

    permission_classes = [IsStaffOrReadOnly]

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
    ordering_fields = ["price", "created_at", "discount", "views"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return ProductWriteSerializer
        return ProductReadSerializer

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a product."""
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class WeightViewSet(viewsets.ModelViewSet):
    """ViewSet definition for ProductWeight."""

    model = ProductWeight
    queryset = ProductWeight.objects.all()

    serializer_class = WeightSerializer

    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [filters.OrderingFilter]

    ordering_fields = ["modified_at"]
