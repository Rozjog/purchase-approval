
from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html

from approvals.models import Approval
from .models import Request


class ApprovalInline(admin.TabularInline):
    model = Approval
    fields = ("employee", "status")
    readonly_fields = ("employee", "status")
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "amount",
        "contractor",
        "employee",
        "status",
        "requires_director",
        "approvals_count",
        "site_link",
    )

    list_display_links = ("name",)
    list_editable = ("contractor",)

    readonly_fields = (
        "id",
        "slug",
        "requires_director",
    )

    search_fields = (
        "name",
        "contractor",
        "employee__name",
    )

    list_filter = (
        "status",
        "employee",
        "requires_director",
    )

    ordering = ("id",)
    list_per_page = 20
    list_select_related = ("employee",)
    autocomplete_fields = ("employee",)

    inlines = (ApprovalInline,)
    view_on_site = True

    actions = (
        "cancel_selected_requests",
        "restore_selected_requests",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            approvals_count=Count("approvals")
        )

    @admin.display(
        description="Количество согласований",
        ordering="approvals_count",
    )
    def approvals_count(self, obj):
        return obj.approvals_count

    @admin.display(description="Страница на сайте")
    def site_link(self, obj):
        if not obj.slug:
            return "—"

        return format_html(
            '<a href="{}" target="_blank">Открыть</a>',
            obj.get_absolute_url(),
        )

    @admin.action(
        description="Отменить выбранные заявки"
    )
    def cancel_selected_requests(self, request, queryset):
        eligible = queryset.filter(
            status=Request.Status.CREATED,
            approvals__isnull=True,
        )

        count = 0

        for purchase_request in eligible:
            purchase_request.cancel()
            count += 1

        self.message_user(
            request,
            f"Отменено заявок: {count}.",
            level=messages.SUCCESS,
        )

    @admin.action(
        description="Вернуть отменённые заявки в статус «Создана»"
    )
    def restore_selected_requests(self, request, queryset):
        ids = queryset.values_list("pk", flat=True)

        updated = Request.objects.filter(
            pk__in=ids,
            status=Request.Status.CANCELLED,
            approvals__isnull=True,
        ).update(status=Request.Status.CREATED)

        self.message_user(
            request,
            f"Восстановлено заявок: {updated}.",
            level=messages.SUCCESS,
        )
