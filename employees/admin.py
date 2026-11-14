
from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "role")
    list_display_links = ("name",)

    search_fields = ("name", "role")
    list_filter = ("role",)

    ordering = ("name",)
    list_per_page = 20
