import coreapi
import coreschema
from rest_framework import filters

from server.apps.category.models import Category


class PriceAndDiscountRangeFilter(filters.BaseFilterBackend):
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
            coreapi.Field(
                name="discount",
                required=False,
                location="query",
                schema=coreschema.Boolean(title="Discount", description="Discount"),
            ),
        ]

    def filter_queryset(self, request, queryset, view):
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        discount = request.query_params.get("discount")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if discount:
            queryset = queryset.filter(discount__gt=0)

        return queryset


class CategoryFilter(filters.BaseFilterBackend):
    """
    Filter that allows to filter products by categories.
    """

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="category_id",
                required=False,
                location="query",
                schema=coreschema.String(
                    title="Category id", description="Category id"
                ),
            ),
        ]

    def filter_queryset(self, request, queryset, view):
        category_ids = request.query_params.get("category_id").split(",")

        if category_ids:
            for category_id in category_ids:
                category = Category.objects.get(
                    id=category_id
                )
                if category.main_category is None:
                    category_ids += list(
                        category.sub_categories.values_list("id", flat=True)
                    )

            queryset = queryset.filter(category__id__in=category_ids)

        return queryset
