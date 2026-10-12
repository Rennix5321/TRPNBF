"""Статистика использует функцию предметной области ПР3."""
from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from incidents import calculate_statistics
from storage import load_incidents


def statistics(request):
    """Сформировать сводку по статусам и приоритетам."""
    incidents_list = load_incidents(settings.INCIDENTS_FILE)
    summary = calculate_statistics(incidents_list)
    status_items = ""
    for status, count in summary["by_status"].items():
        status_items += (
            f'<li class="list-group-item">{escape(status)}: {count}</li>'
        )
    priority_items = ""
    for priority, count in summary["by_priority"].items():
        priority_items += (
            f'<li class="list-group-item">{escape(priority)}: {count}</li>'
        )
    content = f"""
    <h1>Статистика инцидентов</h1>
    <p class="lead">Всего инцидентов: {summary["total"]}</p>
    <div class="row g-4">
        <section class="col-md-6">
            <h2>По статусам</h2>
            <ul class="list-group">{status_items}</ul>
        </section>
        <section class="col-md-6">
            <h2>По приоритетам</h2>
            <ul class="list-group">{priority_items}</ul>
        </section>
    </div>
    """
    return HttpResponse(page("Учет инцидентов - статистика", content))
