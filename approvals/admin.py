from django.contrib import admin

from decisions.models import Decision
from .models import Approval


class DecisionInline(admin.TabularInline):
    model = Decision
    fields = ("result", "comment")
    readonly_fields = ("result", "comment")
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "request_amount", "employee", "status")
    list_display_links = ("id",)
    search_fields = ("request__name", "employee__name")
    list_filter = ("status",)
    ordering = ("id",)
    list_per_page = 20
    list_select_related = ("request", "employee")
    autocomplete_fields = ("request", "employee")
    readonly_fields = ("id",)

    inlines = (DecisionInline,)

    @admin.display(description="Сумма заявки", ordering="request__amount")
    def request_amount(self, obj):
        return obj.request.amount
