
from django.contrib import admin

from .models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "amount",
        "contractor",
        "employee",
        "status",
    )

    list_display_links = ("name",)

    search_fields = (
        "name",
        "contractor",
        "employee__name",
    )

    list_filter = (
        "status",
        "employee",
    )

    ordering = ("id",)
    list_per_page = 20

    list_select_related = ("employee",)
