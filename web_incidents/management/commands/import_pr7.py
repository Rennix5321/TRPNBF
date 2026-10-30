"""Перенос из data/incidents.sqlite (ПР7) в ORM-БД, без удаления имеющихся записей."""
import sqlite3
from pathlib import Path
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from web_incidents.models import Incident, IncidentUser, Executor


class Command(BaseCommand):
    help = "Импортировать PR7 SQLite в Django ORM (повторный запуск безопасен)"

    def add_arguments(self, parser):
        parser.add_argument('--source', default=str(Path(settings.BASE_DIR) / 'data' / 'incidents.sqlite'))

    @transaction.atomic
    def handle(self, *args, **options):
        source = Path(options['source'])
        if not source.is_file():
            raise CommandError(f'Не найден источник ПР7: {source}')
        connection = sqlite3.connect(f'file:{source}?mode=ro', uri=True)
        connection.row_factory = sqlite3.Row
        try:
            people = list(connection.execute('SELECT id, name FROM users'))
            executors = list(connection.execute('SELECT id, name FROM executors'))
            incidents = list(connection.execute('SELECT * FROM incidents ORDER BY id'))
        except sqlite3.Error as error:
            raise CommandError(f'Ошибка чтения ПР7: {error}') from error
        finally:
            connection.close()
        authors_by_id = {}
        for row in people:
            user, _ = IncidentUser.objects.get_or_create(name=row['name'])
            authors_by_id[row['id']] = user
        executors_by_id = {}
        for row in executors:
            executor, _ = Executor.objects.get_or_create(name=row['name'])
            executors_by_id[row['id']] = executor
        for row in incidents:
            date = datetime.fromisoformat(row['created_at'])
            if timezone.is_naive(date):
                date = timezone.make_aware(date, timezone.get_current_timezone())
            Incident.objects.update_or_create(pk=row['id'], defaults={
                'title': row['title'], 'description': row['description'],
                'user': authors_by_id[row['user_id']],
                'executor': executors_by_id.get(row['executor_id']),
                'priority': row['priority'], 'status': row['status'],
                'created_at': date,
            })
        self.stdout.write(self.style.SUCCESS(f'Перенесено инцидентов: {len(incidents)}'))
