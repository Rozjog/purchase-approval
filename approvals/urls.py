from django.urls import path

from . import views


urlpatterns = [
    path("", views.approvals, name="approvals"),
    path("<int:approval_id>/", views.approval_detail, name="approval_detail"),
]