from django.contrib import admin

from .models import Gallery


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "modified_at", "created_at")
    search_fields = ("title",)
