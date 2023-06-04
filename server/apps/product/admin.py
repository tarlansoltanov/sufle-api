from django.contrib import admin

from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_select_related = ("category",)
    list_display = ("name", "category", "price", "created_at")
    list_filter = ("category",)

    inlines = [ProductImageInline]
