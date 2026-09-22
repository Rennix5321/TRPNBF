"""Ошибки JSON, защита сохранения и совместимость формата ПР2."""
import json
from unittest.mock import patch

import pytest

from storage import load_incidents, save_incidents


@pytest.fixture
def row() -> dict:
    return {"id": 1, "title": "Сбой", "description": "Нет связи",
            "user": "Иван", "executor": None, "priority": 3,
            "status": "Новый", "created_at": "2026-09-15T09:00:00"}


def test_json_round_trip(tmp_path, row):
    file = tmp_path / "incidents.json"
    file.write_text(json.dumps([row]), encoding="utf-8")
    items = load_incidents(file)
    save_incidents(file, items)
    assert json.loads(file.read_text(encoding="utf-8")) == [row]


def test_missing_file(tmp_path):
    assert load_incidents(tmp_path / "missing.json") == []


@pytest.mark.parametrize("data", ["{broken", "{}", "[{}]", "[null]"])
def test_invalid_file(tmp_path, data):
    file = tmp_path / "broken.json"
    file.write_text(data, encoding="utf-8")
    with pytest.raises(ValueError):
        load_incidents(file)
    assert file.read_text(encoding="utf-8") == data


@pytest.mark.parametrize("field,value", [
    ("id", True), ("id", 0), ("priority", True), ("priority", 9),
    ("status", None), ("status", "Закрыт"), ("created_at", None),
    ("created_at", "вчера"), ("executor", " "), ("title", ""),
    ("user", " ")])
def test_invalid_record(tmp_path, row, field, value):
    row[field] = value
    file = tmp_path / "invalid.json"
    original = json.dumps([row])
    file.write_text(original, encoding="utf-8")
    with pytest.raises(ValueError):
        load_incidents(file)
    assert file.read_text(encoding="utf-8") == original


def test_duplicate_ids(tmp_path, row):
    file = tmp_path / "duplicate.json"
    file.write_text(json.dumps([row, row]), encoding="utf-8")
    with pytest.raises(ValueError, match="ID"):
        load_incidents(file)


def test_failed_save_keeps_original(tmp_path, row):
    file = tmp_path / "incidents.json"
    original = json.dumps([row])
    file.write_text(original, encoding="utf-8")
    with patch("storage.os.replace", side_effect=OSError("Нет доступа")):
        with pytest.raises(OSError):
            save_incidents(file, [])
    assert file.read_text(encoding="utf-8") == original
    assert not list(tmp_path.glob("*.tmp"))


def test_invalid_encoding(tmp_path):
    file = tmp_path / "bad.json"
    file.write_bytes(b"\xff")
    with pytest.raises(ValueError):
        load_incidents(file)


def test_shared_object_links_restored(tmp_path, row):
    from models import Executor, Incident, User
    row.update(executor="Анна", status="В работе")
    second = dict(row, id=2)
    file = tmp_path / "links.json"
    file.write_text(json.dumps([row, second]), encoding="utf-8")
    first, other = load_incidents(file)
    assert isinstance(first, Incident)
    assert isinstance(first.user, User)
    assert isinstance(first.executor, Executor)
    assert first.user is other.user
    assert first.executor is other.executor


def test_duplicate_objects_not_saved(tmp_path, row):
    file = tmp_path / "duplicate.json"
    file.write_text(json.dumps([row]), encoding="utf-8")
    original = file.read_bytes()
    item = load_incidents(file)[0]
    with pytest.raises(ValueError):
        save_incidents(file, [item, item])
    assert file.read_bytes() == original
