"""Префикс incidents/ обрабатывается корневым urls.py."""
from django.urls import path

from . import views

app_name = "web_incidents"
urlpatterns = [
    path("", views.incident_list, name="incident_list"),
    path("<int:incident_id>/", views.incident_detail, name="incident_detail"),
]
