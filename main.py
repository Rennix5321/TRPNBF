from datetime import datetime


def get_priority_name(priority):
    if priority == 1:
        return "Низкий"
    elif priority == 2:
        return "Средний"
    elif priority == 3:
        return "Высокий"
    else:
        return "Неизвестный"


def get_incident_status(executor):
    if executor:
        return "В работе"
    return "Новый"


def create_incident(title, description, user, executor, priority):
    created_at = datetime.now()
    priority_name = get_priority_name(priority)
    status = get_incident_status(executor)

    print(f"Инцидент: {title}")
    print(f"Описание: {description}")
    print(f"Пользователь: {user}")
    print(f"Исполнитель: {executor}")
    print(f"Приоритет: {priority_name}")
    print(f"Статус: {status}")
    print(f"Дата регистрации: {created_at}")


incident_title = "Недоступность корпоративного сервера"
description = "Сотрудники не могут подключиться к серверу"
user_name = "Иван Петров"
executor_name = "Алексей Смирнов"
priority = 3

create_incident(
    incident_title,
    description,
    user_name,
    executor_name,
    priority
)