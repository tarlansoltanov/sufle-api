from django.contrib import admin

from .models import Banner, Advert


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "photo", "deadline", "created_at")


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "photo", "category", "created_at")
    list_display_links = ("id", "title", "photo")

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 3:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False
