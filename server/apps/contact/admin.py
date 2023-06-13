from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "phone", "type", "is_read", "created_at")
    list_filter = ("is_read", "type")
    search_fields = ("name", "surname", "phone", "message")
    readonly_fields = ("name", "surname", "phone", "message", "type")
    actions = ("mark_as_read",)

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_as_read.short_description = "Mark selected contacts as read"
