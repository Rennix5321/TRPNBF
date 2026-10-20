"""Независимое от Django ORM подключение к SQLite для ПР7."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "incidents.sqlite"


def get_connection(path=None):
    connection = sqlite3.connect(path or DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def fetch_all(query, params=(), path=None):
    with get_connection(path) as conn:
        return [dict(row) for row in conn.execute(query, params).fetchall()]


def fetch_one(query, params=(), path=None):
    with get_connection(path) as conn:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row is not None else None
