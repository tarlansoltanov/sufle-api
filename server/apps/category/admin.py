from django.contrib import admin

from server.apps.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_select_related = ['main_category']
    list_display = (
        'id',
        'name',
        'main_category',
        'created_at',
    )