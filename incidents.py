"""Функции обработки данных об инцидентах."""
from datetime import datetime

STATUSES = ("Новый", "В работе", "Решен", "Закрыт")
PRIORITIES = {1: "Низкий", 2: "Средний", 3: "Высокий"}

def get_priority_name(priority: int) -> str:
    """Вернуть название приоритета (функция из ПР1)."""
    return PRIORITIES.get(priority, "Неизвестный")

def get_incident_status(executor: str | None) -> str:
    """Определить начальный статус (функция из ПР1)."""
    return "В работе" if executor else "Новый"

def create_incident(title: str, description: str, user: str,
                    executor: str | None, priority: int,
                    incident_id: int = 1) -> dict:
    """Создать словарь инцидента на основе сценария из ПР1."""
    if not title.strip() or not description.strip() or not user.strip():
        raise ValueError("Название, описание и пользователь обязательны")
    if priority not in PRIORITIES:
        raise ValueError("Приоритет должен быть от 1 до 3")
    return {"id": incident_id, "title": title.strip(),
            "description": description.strip(), "user": user.strip(),
            "executor": executor.strip() if executor else None,
            "priority": priority, "status": get_incident_status(executor),
            "created_at": datetime.now().isoformat(timespec="seconds")}

def add_incident(incidents: list[dict], title: str, description: str,
                 user: str, priority: int,
                 executor: str | None = None) -> dict:
    """Добавить новый инцидент в список."""
    incident_id = max((item["id"] for item in incidents), default=0) + 1
    item = create_incident(title, description, user, executor,
                           priority, incident_id)
    incidents.append(item)
    return item

def get_incident(incidents: list[dict], incident_id: int) -> dict:
    """Найти инцидент по идентификатору."""
    for item in incidents:
        if item["id"] == incident_id:
            return item
    raise KeyError(f"Инцидент с ID {incident_id} не найден")

def find_incidents(incidents: list[dict], query: str) -> list[dict]:
    """Найти инциденты по названию или описанию."""
    query = query.casefold().strip()
    return [item for item in incidents
            if query in item["title"].casefold()
            or query in item["description"].casefold()]

def filter_incidents(incidents: list[dict], status: str | None = None,
                     priority: int | None = None) -> list[dict]:
    """Отобрать инциденты по статусу и/или приоритету."""
    if status is not None and status not in STATUSES:
        raise ValueError("Неизвестный статус")
    if priority is not None and priority not in PRIORITIES:
        raise ValueError("Приоритет должен быть от 1 до 3")
    return [item for item in incidents
            if (status is None or item["status"] == status)
            and (priority is None or item["priority"] == priority)]

def sort_incidents(incidents: list[dict], key: str = "created_at",
                   reverse: bool = False) -> list[dict]:
    """Вернуть отсортированный список."""
    if key not in {"id", "title", "priority", "status", "created_at"}:
        raise ValueError("Недопустимое поле сортировки")
    return sorted(incidents, key=lambda item: item[key], reverse=reverse)

def assign_executor(incidents: list[dict], incident_id: int,
                    executor: str) -> dict:
    """Назначить исполнителя и перевести новый инцидент в работу."""
    if not executor.strip():
        raise ValueError("Имя исполнителя не может быть пустым")
    item = get_incident(incidents, incident_id)
    item["executor"] = executor.strip()
    if item["status"] == "Новый":
        item["status"] = "В работе"
    return item

def update_incident_status(incidents: list[dict], incident_id: int,
                           status: str) -> dict:
    """Изменить статус инцидента."""
    if status not in STATUSES:
        raise ValueError(f"Допустимые статусы: {', '.join(STATUSES)}")
    item = get_incident(incidents, incident_id)
    item["status"] = status
    return item

def calculate_statistics(incidents: list[dict]) -> dict:
    """Подсчитать статистику по статусам и приоритетам."""
    by_status = {status: 0 for status in STATUSES}
    by_priority = {name: 0 for name in PRIORITIES.values()}
    for item in incidents:
        by_status[item["status"]] += 1
        by_priority[get_priority_name(item["priority"])] += 1
    return {"total": len(incidents), "by_status": by_status,
            "by_priority": by_priority}
