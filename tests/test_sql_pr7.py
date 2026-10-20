"""Проверки структуры и SQL ПР7 без зависимости от web views."""
import json
import sqlite3
from pathlib import Path

from db.database import fetch_all, get_connection
from db.import_json import import_incidents


def test_import_and_fk(tmp_path):
    source = tmp_path / "input.json"
    source.write_text(json.dumps([
        {"id": 1, "title": "Тест", "description": "Детали",
         "user": "Автор", "executor": None, "priority": 2,
         "status": "Новый", "created_at": "2026-09-15T09:00:00"}
    ], ensure_ascii=False), encoding="utf-8")
    path = tmp_path / "test.sqlite"
    assert import_incidents(source, path) == 1
    assert import_incidents(source, path) == 1
    assert fetch_all("SELECT title FROM incidents", path=path)[0]["title"] == "Тест"
    with get_connection(path) as conn:
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 1
        try:
            conn.execute("INSERT INTO incidents (id,title,description,user_id,priority,status,created_at) VALUES (9,'x','x',999,1,'Новый','2026-01-01')")
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("Внешний ключ не сработал")


def test_query_examples():
    root = Path(__file__).resolve().parents[1]
    contents = (root / "sql" / "queries.sql").read_text(encoding="utf-8")
    statements = [statement.strip() for statement in contents.split(";")
                  if statement.strip()]
    assert len(statements) >= 10
    with get_connection() as conn:
        for statement in statements:
            conn.execute(statement).fetchall()
