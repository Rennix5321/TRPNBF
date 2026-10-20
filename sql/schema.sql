-- ПР7. Схема системы учета инцидентов. Повторный запуск безопасен.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS executors (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS incidents (
 id INTEGER PRIMARY KEY, title TEXT NOT NULL,
 description TEXT NOT NULL, user_id INTEGER NOT NULL,
 executor_id INTEGER, priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 3),
 status TEXT NOT NULL CHECK (status IN ('Новый','В работе','Решен','Закрыт')),
 created_at TEXT NOT NULL,
 FOREIGN KEY (user_id) REFERENCES users(id),
 FOREIGN KEY (executor_id) REFERENCES executors(id)
);
