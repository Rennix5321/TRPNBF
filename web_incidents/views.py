"""ПР9: страницы работают через Django ORM; старый JSON-слой сохранён."""
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from incidents import find_incident_by_id
from storage import load_incidents
from .models import Incident


def incident_list(request):
    # Историческая страница ПР6 для сравнения исходного JSON и ORM.
    items = load_incidents(settings.INCIDENTS_FILE)
    return render(request, 'web_incidents/incident_list.html', {
        'incidents': items, 'page_title': 'Инциденты JSON'})


def incident_detail(request, incident_id):
    # Детальная страница теперь использует ORM; источник ПР7 больше не нужен.
    incident = get_object_or_404(
        Incident.objects.select_related('user', 'executor'), pk=incident_id)
    return render(request, 'web_incidents/incident_detail.html', {
        'incident': incident, 'page_title': incident.title})


def sql_incident_list(request):
    # URL ПР7 оставлен совместимым; реализация ПР9 на ORM.
    qs = Incident.objects.select_related('user', 'executor').order_by('id')
    page = Paginator(qs, 10).get_page(request.GET.get('page'))
    return render(request, 'web_incidents/sql_list.html', {
        'incidents': page, 'page_obj': page,
        'page_title': 'Инциденты ORM'})


def sql_search(request):
    statuses = ('Все', 'Новый', 'В работе', 'Решен', 'Закрыт')
    status = request.GET.get('status', 'Все')
    if status not in statuses:
        status = 'Все'
    priority = request.GET.get('priority', '')
    if priority not in ('', '1', '2', '3'):
        priority = ''
    title = request.GET.get('q', '').strip()[:100]
    author = request.GET.get('author', '').strip()[:100]
    sort = request.GET.get('sort', 'id')
    sort_fields = {'id': 'id', 'newest': '-created_at',
                   'priority': '-priority', 'title': 'title'}
    if sort not in sort_fields:
        sort = 'id'
    qs = Incident.objects.select_related('user', 'executor')
    if title:
        qs = qs.filter(Q(title__icontains=title) |
                       Q(description__icontains=title))
    if author:
        qs = qs.filter(user__name__icontains=author)
    if status != 'Все':
        qs = qs.filter(status=status)
    if priority:
        qs = qs.filter(priority=int(priority))
    qs = qs.order_by(sort_fields[sort], 'id')
    page = Paginator(qs, 10).get_page(request.GET.get('page'))
    return render(request, 'web_incidents/sql_search.html', {
        'incidents': page, 'page_obj': page, 'status': status,
        'statuses': statuses, 'priority': priority, 'q': title,
        'author': author, 'sort': sort, 'page_title': 'Поиск ORM'})
