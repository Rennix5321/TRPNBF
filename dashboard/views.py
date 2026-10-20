"""Статистика прежней JSON-версии и агрегаты из SQLite."""
from django.conf import settings
from django.shortcuts import render
from incidents import calculate_statistics
from storage import load_incidents
from db.database import fetch_all, fetch_one


def statistics(request):
    summary = calculate_statistics(load_incidents(settings.INCIDENTS_FILE))
    return render(request, "dashboard/statistics.html", {
        "summary": summary, "page_title": "Статистика JSON"})


def sql_statistics(request):
    by_status = fetch_all("""SELECT status, COUNT(*) AS total
                             FROM incidents GROUP BY status
                             ORDER BY total DESC, status""")
    by_priority = fetch_all("""SELECT priority, COUNT(*) AS total
                               FROM incidents GROUP BY priority
                               ORDER BY priority""")
    by_author = fetch_all("""SELECT u.name AS author_name,
                                  COUNT(i.id) AS total
                            FROM users u LEFT JOIN incidents i
                            ON i.user_id = u.id
                            GROUP BY u.id, u.name
                            ORDER BY total DESC""")
    total = fetch_one("SELECT COUNT(*) AS total FROM incidents")
    return render(request, "dashboard/sql_statistics.html", {
        "by_status": by_status, "by_priority": by_priority,
        "by_author": by_author, "total": total["total"],
        "page_title": "Статистика SQLite"})
