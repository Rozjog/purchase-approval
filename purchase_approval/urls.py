
from django.conf import settings
from django.contrib import admin
from django.urls import include, path


admin.site.site_header = "Purchase Approval"
admin.site.site_title = "Purchase Approval — администрирование"
admin.site.index_title = "Управление системой закупок"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("employees/", include("employees.urls")),
    path("requests/", include("purchase_requests.urls")),
    path("approvals/", include("approvals.urls")),
    path("decisions/", include("decisions.urls")),
]


if settings.DEBUG:
    urlpatterns += [
        path(
            "__debug__/",
            include("debug_toolbar.urls"),
        ),
    ]


handler404 = "homepage.views.page_not_found"
