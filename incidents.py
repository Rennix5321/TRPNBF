"""Функции обработки данных об инцидентах."""
from models import Executor, Incident, User
from models.incident import PRIORITIES, STATUSES


def get_priority_name(priority: int) -> str:
    """Вернуть название приоритета (функция из ПР1)."""
    return PRIORITIES.get(priority, "Неизвестный")


def create_incident(title: str, description: str, user: User,
                    executor: Executor | None, priority: int,
                    incident_id: int = 1) -> Incident:
    """Создать объект вместо словаря ПР2."""
    return Incident(incident_id, title, description, user, priority, executor)


def add_incident(incidents: list[Incident], title: str, description: str,
                 user: User, priority: int,
                 executor: Executor | None = None) -> Incident:
    """Добавить новый инцидент в список."""
    incident_id = max((item.id for item in incidents), default=0) + 1
    item = create_incident(title, description, user, executor,
                           priority, incident_id)
    incidents.append(item)
    return item


def get_incident(incidents: list[Incident], incident_id: int) -> Incident:
    """Найти инцидент по идентификатору."""
    for item in incidents:
        if item.id == incident_id:
            return item
    raise KeyError(f"Инцидент с ID {incident_id} не найден")


def find_incidents(incidents: list[Incident], query: str) -> list[Incident]:
    """Найти инциденты по названию или описанию."""
    query = query.casefold().strip()
    return [item for item in incidents
            if query in item.title.casefold()
            or query in item.description.casefold()]


def filter_incidents(incidents: list[Incident], status: str | None = None,
                     priority: int | None = None) -> list[Incident]:
    """Отобрать инциденты по статусу и/или приоритету."""
    if status is not None and status not in STATUSES:
        raise ValueError("Неизвестный статус")
    if priority is not None and (
            type(priority) is not int or priority not in PRIORITIES):
        raise ValueError("Приоритет должен быть от 1 до 3")
    return [item for item in incidents
            if (status is None or item.status == status)
            and (priority is None or item.priority == priority)]


def sort_incidents(incidents: list[Incident], key: str = "created_at",
                   reverse: bool = False) -> list[Incident]:
    """Вернуть отсортированный список."""
    if key not in {"id", "title", "priority", "status", "created_at"}:
        raise ValueError("Недопустимое поле сортировки")
    return sorted(incidents, key=lambda item: getattr(item, key),
                  reverse=reverse)


def calculate_statistics(incidents: list[Incident]) -> dict:
    """Подсчитать статистику по статусам и приоритетам."""
    by_status = {status: 0 for status in STATUSES}
    by_priority = {name: 0 for name in PRIORITIES.values()}
    for item in incidents:
        by_status[item.status] += 1
        by_priority[get_priority_name(item.priority)] += 1
    return {"total": len(incidents), "by_status": by_status,
            "by_priority": by_priority}
