from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("employees/", include("employees.urls")),
    path("requests/", include("purchase_requests.urls")),
    path("approvals/", include("approvals.urls")),
    path("decisions/", include("decisions.urls")),
]
