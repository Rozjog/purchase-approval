
from django.contrib import admin

from .models import Approval


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "request",
        "employee",
        "status",
    )

    list_display_links = ("id",)

    search_fields = (
        "request__name",
        "employee__name",
    )

    list_filter = ("status",)

    ordering = ("id",)
    list_per_page = 20

    list_select_related = (
        "request",
        "employee",
    )
