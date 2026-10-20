"""Импорт JSON-данных в связанную реляционную SQLite-базу."""
import argparse
from pathlib import Path
from storage import load_incidents
from db.database import DB_PATH, get_connection

ROOT = Path(__file__).resolve().parent.parent


def import_incidents(source=None, destination=None):
    source = Path(source or ROOT / "data" / "incidents.json")
    destination = Path(destination or DB_PATH)
    destination.parent.mkdir(parents=True, exist_ok=True)
    incidents = load_incidents(source)
    authors = sorted({item.user.name for item in incidents})
    executors = sorted({item.executor.name for item in incidents
                        if item.executor is not None})
    with get_connection(destination) as conn:
        conn.executescript((ROOT / "sql" / "schema.sql").read_text(
            encoding="utf-8"))
        # Удаление дочерних записей раньше родительских предотвращает ошибки FK.
        conn.execute("DELETE FROM incidents")
        conn.execute("DELETE FROM users")
        conn.execute("DELETE FROM executors")
        conn.executemany("INSERT INTO users(name) VALUES (?)",
                         [(name,) for name in authors])
        conn.executemany("INSERT INTO executors(name) VALUES (?)",
                         [(name,) for name in executors])
        users = {row["name"]: row["id"] for row in conn.execute(
            "SELECT id, name FROM users")}
        workers = {row["name"]: row["id"] for row in conn.execute(
            "SELECT id, name FROM executors")}
        conn.executemany("""INSERT INTO incidents
            (id, title, description, user_id, executor_id, priority,
             status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", [
            (item.id, item.title, item.description, users[item.user.name],
             workers[item.executor.name] if item.executor else None,
             item.priority, item.status, item.created_at)
            for item in incidents])
        conn.commit()
    return len(incidents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path)
    parser.add_argument("--destination", type=Path)
    arguments = parser.parse_args()
    print("Импортировано инцидентов:", import_incidents(
        arguments.source, arguments.destination))
