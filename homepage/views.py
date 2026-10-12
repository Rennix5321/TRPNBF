"""Главная страница, общий HTML-каркас и обработчик 404."""
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import escape

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)


def page(title, content):
    """Общий HTML; content содержит разметку, данные экранируются во views."""
    home_url = reverse("homepage:index")
    incidents_url = reverse("web_incidents:incident_list")
    statistics_url = reverse("dashboard:statistics")
    return f"""<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link href="{BOOTSTRAP_CSS}" rel="stylesheet">
    <style>
        body {{ background: #f4f6fa; color: #172338;
                font-family: system-ui, sans-serif; margin: 0; }}
        main {{ max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }}
        nav {{ padding: 1rem; background: #172338; }}
        nav a {{ color: white; margin-right: 1rem; }}
        .description {{ white-space: pre-wrap; overflow-wrap: anywhere; }}
        a:focus-visible {{ outline: 3px solid #ffbf47; }}
    </style>
</head>
<body>
    <nav aria-label="Основная навигация">
        <a href="{home_url}" class="fw-bold">Учет инцидентов</a>
        <a href="{incidents_url}">Инциденты</a>
        <a href="{statistics_url}">Статистика</a>
    </nav>
    <main class="container">{content}</main>
    <footer class="container text-muted pb-4">Система учета инцидентов</footer>
</body>
</html>"""


def index(request):
    """GET /: описание системы и переходы к данным."""
    incidents_url = reverse("web_incidents:incident_list")
    statistics_url = reverse("dashboard:statistics")
    content = f"""
    <h1 class="display-4">Система учета инцидентов</h1>
    <p class="lead">Просмотр обращений, исполнителей и статусов.</p>
    <p>Выберите раздел для просмотра данных системы.</p>
    <a href="{incidents_url}" class="btn btn-primary me-2">Инциденты</a>
    <a href="{statistics_url}" class="btn btn-secondary">Статистика</a>
    """
    return HttpResponse(page("Учет инцидентов - главная", content))


def page_not_found(request, exception):
    """Общий handler404: используется Django при DEBUG=False."""
    home_url = reverse("homepage:index")
    content = f"""
    <h1 class="text-danger">404 - страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="{home_url}" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(page("404 - страница не найдена", content),
                        status=404)
