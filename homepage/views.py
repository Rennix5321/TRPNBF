"""Главная страница и обработчик отсутствующих маршрутов."""
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import escape

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)


def page(title, content):
    """Совместимость со старыми проверками ПР5; Django views не используют."""
    return (f'<html lang="ru"><title>{escape(title)}</title>'
            f'<body>{content}</body></html>')


def index(request):
    return render(request, "homepage/index.html", {
        "page_title": "Система учета инцидентов"})


def page_not_found(request, exception):
    return render(request, "homepage/404.html", status=404)
