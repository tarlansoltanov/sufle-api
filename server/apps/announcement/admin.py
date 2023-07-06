from django.contrib import admin

from .models import Banner, Advert


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "photo", "deadline", "created_at")


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ("id", "photo", "title", "category", "created_at")
