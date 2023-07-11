from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from server.apps.core.pagination import CustomPagination

from .models import Product, ProductWeight
from .logic.serializers import (
    ProductReadSerializer,
    ProductWriteSerializer,
    WeightReadSerializer,
)
from .logic.filters import PriceAndDiscountRangeFilter, CategoryFilter


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet definition for Product."""

    model = Product
    queryset = (
        Product.objects.select_related("category")
        .prefetch_related("images")
        .all()
        .order_by("-modified_at")
    )
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

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super(self.__class__, self).get_permissions()

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a product."""
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class WeightViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet definition for ProductWeight."""

    model = ProductWeight
    serializer_class = WeightReadSerializer
    queryset = ProductWeight.objects.all().order_by("person_count")
    permission_classes = [permissions.AllowAny]
