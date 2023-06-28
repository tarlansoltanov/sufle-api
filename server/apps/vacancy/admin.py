from django.contrib import admin

from .models import Vacancy, Requirement


class RequirementInline(admin.TabularInline):
    model = Requirement


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "created_at")
    search_fields = ("name", "title")
    inlines = [RequirementInline]
