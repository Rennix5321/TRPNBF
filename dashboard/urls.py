"""Пространство имён статистики."""
from django.urls import path
from . import views
app_name = "dashboard"
urlpatterns = [path("", views.statistics, name="statistics"),
               path("sql/", views.sql_statistics, name="sql_statistics")]
