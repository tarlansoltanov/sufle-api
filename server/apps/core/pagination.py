from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "limit"
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get("limit") == "all":
            return None
        return super().paginate_queryset(queryset, request, view)
