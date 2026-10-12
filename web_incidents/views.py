"""Веб-представления используют объекты и JSON-хранилище ПР3."""
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import escape

from homepage.views import page
from incidents import find_incident_by_id
from storage import load_incidents


def incident_list(request):
    """Загрузить объекты Incident и сформировать ссылки на карточки."""
    items = ""
    for incident in load_incidents(settings.INCIDENTS_FILE):
        detail_url = reverse("web_incidents:incident_detail",
                             args=[incident.id])
        items += f"""
        <li class="list-group-item">
            <a href="{detail_url}">{escape(incident.title)}</a>
            <span class="badge bg-secondary">{escape(incident.status)}</span>
            <span class="text-muted">{escape(incident.priority_name)}</span>
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Инциденты пока отсутствуют.</li>'
    content = f"""
    <h1>Инциденты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Учет инцидентов - список", content))


def incident_detail(request, incident_id):
    """Числовой ID из URL -> объект Incident -> HTML или HTTP 404."""
    incidents_list = load_incidents(settings.INCIDENTS_FILE)
    incident = find_incident_by_id(incidents_list, incident_id)
    list_url = reverse("web_incidents:incident_list")
    if incident is None:
        content = f"""
        <h1 class="text-danger">Инцидент не найден</h1>
        <p>Инцидент с указанным ID отсутствует в системе.</p>
        <a href="{list_url}" class="btn btn-outline-secondary">
            К списку инцидентов
        </a>
        """
        return HttpResponse(page("Инцидент не найден", content), status=404)

    executor = incident.executor.name if incident.executor else "Не назначен"
    content = f"""
    <article class="card">
        <div class="card-body">
            <h1 class="card-title">{escape(incident.title)}</h1>
            <p><strong>ID:</strong> {incident.id}</p>
            <p class="description">{escape(incident.description)}</p>
            <p><strong>Автор:</strong> {escape(incident.user.name)}</p>
            <p><strong>Исполнитель:</strong> {escape(executor)}</p>
            <p><strong>Приоритет:</strong>
                {incident.priority} - {escape(incident.priority_name)}</p>
            <p><strong>Статус:</strong>
                <span class="badge bg-secondary">
                    {escape(incident.status)}
                </span>
            </p>
            <p><strong>Дата регистрации:</strong>
                {escape(incident.created_at)}</p>
            <a href="{list_url}" class="btn btn-outline-secondary">
                К списку инцидентов
            </a>
        </div>
    </article>
    """
    return HttpResponse(page(incident.title, content), status=200)
