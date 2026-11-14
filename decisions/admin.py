
from django.contrib import admin

from .models import Decision


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "approval",
        "result",
        "comment",
    )

    list_display_links = ("id",)

    search_fields = (
        "approval__request__name",
        "result",
        "comment",
    )

    list_filter = ("result",)

    ordering = ("id",)
    list_per_page = 20

    list_select_related = ("approval",)
