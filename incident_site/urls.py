"""Корневые маршруты и общий обработчик 404."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("incidents/", include("web_incidents.urls")),
    path("statistics/", include("dashboard.urls")),
    path("", include("homepage.urls")),
]
handler404 = "homepage.views.page_not_found"
