from django.contrib import admin

from server.apps.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_select_related = ["main_category"]
    list_display = (
        "name",
        "is_main",
        "main_category",
        "modified_at",
        "created_at",
    )

    def get_queryset(self, request):
        return super(CategoryAdmin, self).get_queryset(request).order_by("-modified_at")

    def is_main(self, obj):
        return obj.main_category is None

    def get_form(self, request, obj, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["main_category"].queryset = Category.objects.filter(
            main_category=None
        )
        return form
