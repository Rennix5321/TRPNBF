"""Пространство имён страниц инцидентов."""
from django.urls import path
from . import views
app_name = "web_incidents"
urlpatterns = [
    path("", views.incident_list, name="incident_list"),
    path("sql/", views.sql_incident_list, name="sql_list"),
    path("search/", views.sql_search, name="sql_search"),
    path("<int:incident_id>/", views.incident_detail, name="incident_detail"),
]
