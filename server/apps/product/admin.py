from django.contrib import admin

from .models import Product, ProductImage, ProductWeight


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_select_related = ("category",)
    list_display = ("name", "category", "price", "created_at")
    list_filter = ("category",)

    inlines = [ProductImageInline]


@admin.register(ProductWeight)
class ProductWeightAdmin(admin.ModelAdmin):
    list_display = ("person_count", "weight")
