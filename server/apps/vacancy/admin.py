from django.contrib import admin

from .models import Vacancy, Requirement


class RequirementInline(admin.TabularInline):
    model = Requirement


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "is_active", "created_at")
    filter_fields = ("is_active",)
    search_fields = ("name", "title")
    inlines = [RequirementInline]
