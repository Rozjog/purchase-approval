from django.urls import path
from . import views


app_name = "approvals"

urlpatterns = [
    path("", views.approvals, name="approvals"),
    path("<int:approval_id>/", views.approval_detail, name="approval_detail"),
]
