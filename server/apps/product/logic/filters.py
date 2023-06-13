import coreapi
import coreschema
from rest_framework import filters

from server.apps.category.models import Category


class PriceRangeFilter(filters.BaseFilterBackend):
    """
    Filter that allows to filter products by price range.
    """

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="min_price",
                required=False,
                location="query",
                schema=coreschema.Integer(
                    title="Minimum price", description="Minimum price"
                ),
            ),
            coreapi.Field(
                name="max_price",
                required=False,
                location="query",
                schema=coreschema.Integer(
                    title="Maximum price", description="Maximum price"
                ),
            ),
        ]

    def filter_queryset(self, request, queryset, view):
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class CategoryFilter(filters.BaseFilterBackend):
    """
    Filter that allows to filter products by category.
    """

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="category_id",
                required=False,
                location="query",
                schema=coreschema.Integer(
                    title="Category ID", description="Category ID"
                ),
            ),
        ]

    def filter_queryset(self, request, queryset, view):
        if category_id := request.query_params.get("category_id"):
            category = Category.objects.get(id=category_id)
            queryset = queryset.filter(
                category__in=[*category.sub_categories.all(), category]
            )

        return queryset
