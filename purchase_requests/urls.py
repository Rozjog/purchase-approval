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
        "create/",
        views.request_create,
        name="request_create",
    ),
    path(
        "<int:request_id>/edit/",
        views.request_update,
        name="request_update",
    ),
    path(
        "<int:request_id>/cancel/",
        views.request_cancel,
        name="request_cancel",
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
