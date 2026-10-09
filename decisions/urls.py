from django.urls import path

from . import views


urlpatterns = [
    path("", views.decisions, name="decisions"),
    path("<int:decision_id>/", views.decision_detail, name="decision_detail"),
]
