
from django.urls import path

from . import views


app_name = "purchase_requests"

urlpatterns = [
    path(
        "",
        views.requests,
        name="requests",
    ),
    path(
        "statistics/",
        views.statistics,
        name="statistics",
    ),
    path(
        "<int:request_id>/",
        views.request_detail_by_id,
        name="request_detail_by_id",
    ),
    path(
        "<slug:slug>/",
        views.request_detail,
        name="request_detail",
    ),
]
