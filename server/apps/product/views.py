from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from server.apps.core.pagination import CustomPagination

from .models import Product
from .logic.serializers import ProductReadSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    model = Product
    serializer_class = ProductReadSerializer
    queryset = (
        Product.objects.select_related("category").prefetch_related("images").all()
    )
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "is_new"]
    search_fields = ["name", "category__name"]
    ordering_fields = ["price", "created_at"]

    def get_serializer_context(self):
        context = super(ProductViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=False, methods=["GET"])
    def new(self, request):
        """Get new products."""
        products = self.queryset.filter(is_new=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
