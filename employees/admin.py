from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "role", "requests_count")
    list_display_links = ("name",)
    search_fields = ("name", "role")
    list_filter = ("role",)
    ordering = ("name",)
    list_per_page = 20

    def get_queryset(self, request):
        from django.db.models import Count

        queryset = super().get_queryset(request)
        return queryset.annotate(_requests_count=Count("requests"))

    @admin.display(description="Количество заявок", ordering="_requests_count")
    def requests_count(self, obj):
        return obj._requests_count
