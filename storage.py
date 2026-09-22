"""Преобразование JSON ПР2 в объекты и обратно."""
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from models import Executor, Incident, User


def load_incidents(filename: str | Path) -> list[Incident]:
    """Загрузить объекты, восстановив общие ссылки на людей по имени/роли."""
    try:
        with Path(filename).open(encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError("Поврежден JSON: исходный файл сохранен") from error
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список инцидентов")
    return decode_incidents(data)


def decode_incidents(data: list) -> list[Incident]:
    """Проверить записи и восстановить связанные объекты."""
    users: dict[str, User] = {}
    executors: dict[str, Executor] = {}
    incidents = []
    ids = set()
    for row in data:
        try:
            if not isinstance(row, dict):
                raise ValueError("Запись должна быть словарем")
            if not isinstance(row["created_at"], str):
                raise ValueError("Дата должна быть строкой, не null")
            if not isinstance(row["status"], str):
                raise ValueError("Статус должен быть строкой, не null")
            user = User(row["user"])
            user = users.setdefault(user.name, user)
            executor = None
            if row["executor"] is not None:
                executor = Executor(row["executor"])
                executor = executors.setdefault(executor.name, executor)
            item = Incident(row["id"], row["title"], row["description"],
                            user, row["priority"], executor,
                            row["created_at"], row["status"])
            if item.id in ids:
                raise ValueError("Повторяющийся ID")
            ids.add(item.id)
            incidents.append(item)
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                f"Некорректная запись инцидента: {error}") from error
    return incidents


def save_incidents(filename: str | Path,
                   incidents: list[Incident]) -> None:
    """Атомарно сохранить объекты в совместимом с ПР2 формате JSON."""
    data = [{"id": item.id, "title": item.title,
             "description": item.description, "user": item.user.name,
             "executor": item.executor.name if item.executor else None,
             "priority": item.priority, "status": item.status,
             "created_at": item.created_at} for item in incidents]
    decode_incidents(data)
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", delete=False,
                                dir=path.parent, suffix=".tmp") as file:
            temporary = Path(file.name)
            json.dump(data, file, ensure_ascii=False, indent=2)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
