"""ПР9: тесты ORM, связей, отображения, фильтрации и пагинации."""
import pytest
from datetime import datetime, timezone
from django.urls import reverse
from web_incidents.models import Incident, IncidentUser, Executor

pytestmark = pytest.mark.django_db

@pytest.fixture
def populated():
    user = IncidentUser.objects.create(name='Автор теста')
    worker = Executor.objects.create(name='Исполнитель теста')
    return Incident.objects.create(title='Падение сервера', description='Не работает',
        user=user, executor=worker, priority=3, status='Новый',
        created_at=datetime(2026, 9, 15, tzinfo=timezone.utc))

def test_orm_crud(populated):
    assert Incident.objects.get(pk=populated.pk).title == 'Падение сервера'
    populated.status = 'Решен'
    populated.save(update_fields=['status'])
    assert Incident.objects.filter(status='Решен').count() == 1
    populated.delete()
    assert Incident.objects.count() == 0

def test_search_and_detail(client, populated):
    response = client.get(reverse('web_incidents:sql_search'), {'q': 'сервер', 'priority': '3'})
    assert response.status_code == 200
    assert b'html' in response.content.lower()
    assert client.get(reverse('web_incidents:incident_detail', args=[populated.pk])).status_code == 200
    assert client.get(reverse('web_incidents:incident_detail', args=[99999])).status_code == 404

def test_invalid_sort_does_not_crash(client, populated):
    assert client.get(reverse('web_incidents:sql_search'), {'sort': 'bad_field'}).status_code == 200

def test_stats_empty(client):
    assert client.get(reverse('dashboard:sql_statistics')).status_code == 200
