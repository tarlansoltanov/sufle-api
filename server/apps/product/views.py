from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Product
from .logic.serializers import ProductReadSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    model = Product
    serializer_class = ProductReadSerializer
    queryset = (
        Product.objects.select_related("category").prefetch_related("images").all()
    )
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        context = super(ProductViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
