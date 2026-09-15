"""Загрузка и сохранение данных в JSON."""
import json
from pathlib import Path

def load_incidents(filename: str | Path) -> list[dict]:
    """Загрузить инциденты; при отсутствии файла вернуть пустой список."""
    path = Path(filename)
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(f"Некорректный JSON в файле {path}") from error
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список инцидентов")
    return data

def save_incidents(filename: str | Path, incidents: list[dict]) -> None:
    """Сохранить инциденты, создав каталог при необходимости."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(incidents, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise OSError(f"Не удалось сохранить файл {path}") from error
