"""Инциденты: исходные объекты JSON и SQL-представления ПР7."""
from django.conf import settings
from django.shortcuts import render
from incidents import find_incident_by_id
from storage import load_incidents
from db.database import fetch_all, fetch_one


def incident_list(request):
    items = load_incidents(settings.INCIDENTS_FILE)
    return render(request, "web_incidents/incident_list.html", {
        "incidents": items, "page_title": "Инциденты"})


def incident_detail(request, incident_id):
    item = find_incident_by_id(
        load_incidents(settings.INCIDENTS_FILE), incident_id)
    if item is None:
        return render(request, "web_incidents/incident_missing.html",
                      status=404)
    return render(request, "web_incidents/incident_detail.html", {
        "incident": item, "page_title": item.title})


def sql_incident_list(request):
    """Список записей исключительно из SQLite, независимо от JSON."""
    items = fetch_all("""SELECT i.id, i.title, i.status, i.priority,
                              u.name AS author_name,
                              e.name AS executor_name
                       FROM incidents i
                       JOIN users u ON u.id = i.user_id
                       LEFT JOIN executors e ON e.id = i.executor_id
                       ORDER BY i.id""")
    return render(request, "web_incidents/sql_list.html", {
        "incidents": items, "page_title": "Инциденты из SQLite"})


def sql_search(request):
    """Поиск по пользовательскому параметру с безопасной подстановкой."""
    statuses = ("Все", "Новый", "В работе", "Решен", "Закрыт")
    status = request.GET.get("status", "Все")
    if status not in statuses:
        status = "Все"
    priority = request.GET.get("priority", "")
    if priority not in ("", "1", "2", "3"):
        priority = ""
    title = request.GET.get("q", "").strip()[:100]
    conditions = ["i.title LIKE ?"]
    params = [f"%{title}%"]
    if status != "Все":
        conditions.append("i.status = ?")
        params.append(status)
    if priority:
        conditions.append("i.priority = ?")
        params.append(int(priority))
    query = ("SELECT i.id, i.title, i.status, i.priority, "
             "u.name AS author_name, e.name AS executor_name "
             "FROM incidents i JOIN users u ON u.id = i.user_id "
             "LEFT JOIN executors e ON e.id = i.executor_id "
             "WHERE " + " AND ".join(conditions) + " ORDER BY i.id")
    items = fetch_all(query, params)
    return render(request, "web_incidents/sql_search.html", {
        "incidents": items, "status": status, "statuses": statuses,
        "priority": priority, "q": title,
        "page_title": "Поиск в SQLite"})
