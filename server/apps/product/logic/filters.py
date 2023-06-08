import coreapi
import coreschema
from rest_framework import filters


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
