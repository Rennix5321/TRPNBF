"""15+ содержательных ORM-запросов ПР9 для защиты (вызываются из Django shell).

Каждый пример реализует отдельный пользовательский сценарий.
"""
from django.db.models import Q, Count, Avg, Max
from .models import Incident, IncidentUser, Executor


def example_queries():
    return {
        'all_incidents': Incident.objects.all(),
        'by_id': Incident.objects.filter(pk=1),
        'new_incidents': Incident.objects.filter(status='Новый'),
        'high_priority_active': Incident.objects.filter(priority=3).exclude(status='Закрыт'),
        'by_author': Incident.objects.filter(user__name__icontains='Иван'),
        'without_executor': Incident.objects.filter(executor__isnull=True),
        'exclude_closed': Incident.objects.exclude(status='Закрыт'),
        'title_search': Incident.objects.filter(title__icontains='сервер'),
        'multi_field_search': Incident.objects.filter(Q(title__icontains='ошибка') | Q(description__icontains='ошибка')),
        'by_date': Incident.objects.order_by('-created_at'),
        'by_priority_and_date': Incident.objects.order_by('-priority', '-created_at'),
        'with_related': Incident.objects.select_related('user', 'executor'),
        'users_with_counts': IncidentUser.objects.annotate(total=Count('incidents')),
        'statuses_with_counts': Incident.objects.values('status').annotate(total=Count('id')),
        'priority_average': Incident.objects.aggregate(average=Avg('priority')),
        'max_priority': Incident.objects.aggregate(maximum=Max('priority')),
        'most_active_authors': IncidentUser.objects.annotate(total=Count('incidents')).order_by('-total'),
        'executors_with_counts': Executor.objects.annotate(total=Count('incidents')),
    }
