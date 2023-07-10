import coreapi
import coreschema
from rest_framework import filters


class CategoryTypeFilter(filters.BaseFilterBackend):
    """
    Filter that allows to filter category by type.
    """

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name="type",
                required=False,
                location="query",
                schema=coreschema.String(title="Type", description="Type"),
            ),
        ]

    def filter_queryset(self, request, queryset, view):
        try:
            category_type = request.query_params.get("type")
        except Exception:
            category_type = None

        if category_type == "main":
            queryset = queryset.prefetch_related("sub_categories").filter(
                main_category=None
            )
        elif category_type == "sub":
            queryset = queryset.select_related("main_category").exclude(
                main_category=None
            )
        else:
            queryset = queryset.prefetch_related("sub_categories").select_related(
                "main_category"
            )

        return queryset
