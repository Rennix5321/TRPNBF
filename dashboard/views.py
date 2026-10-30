"""Статистика JSON (ПР6) и ORM (ПР9)."""
from django.conf import settings
from django.db.models import Count, Avg
from django.shortcuts import render
from incidents import calculate_statistics
from storage import load_incidents
from web_incidents.models import Incident, IncidentUser


def statistics(request):
    summary = calculate_statistics(load_incidents(settings.INCIDENTS_FILE))
    return render(request, 'dashboard/statistics.html', {
        'summary': summary, 'page_title': 'Статистика JSON'})


def sql_statistics(request):
    by_status = Incident.objects.values('status').annotate(
        total=Count('id')).order_by('-total', 'status')
    by_priority = Incident.objects.values('priority').annotate(
        total=Count('id')).order_by('priority')
    by_author = IncidentUser.objects.annotate(
        total=Count('incidents')).values('name', 'total').order_by('-total')
    summary = Incident.objects.aggregate(total=Count('id'), avg_priority=Avg('priority'))
    return render(request, 'dashboard/sql_statistics.html', {
        'by_status': by_status, 'by_priority': by_priority,
        'by_author': [{'author_name': x['name'], 'total': x['total']}
                      for x in by_author],
        'total': summary['total'], 'avg_priority': summary['avg_priority'],
        'page_title': 'Статистика ORM'})
