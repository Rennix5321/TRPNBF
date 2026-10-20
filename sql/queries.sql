-- ПР7. Запросы для учебной защиты: минимум 2 SELECT, WHERE, JOIN,
-- агрегатных функций и GROUP BY. Параметры в Django передаются через ?.
-- 1. SELECT: все инциденты
SELECT id, title, status FROM incidents ORDER BY id;
-- 2. SELECT: список авторов
SELECT id, name FROM users ORDER BY name;
-- 3. WHERE: инциденты высокого приоритета
SELECT id, title, priority FROM incidents WHERE priority >= 3;
-- 4. WHERE: активные инциденты
SELECT id, title, status FROM incidents WHERE status IN ('Новый', 'В работе');
-- 5. JOIN: инциденты и авторы
SELECT i.id, i.title, u.name AS author FROM incidents i JOIN users u ON i.user_id = u.id;
-- 6. JOIN: инциденты, авторы и исполнители, включая незанятые
SELECT i.title, u.name AS author, e.name AS executor FROM incidents i
JOIN users u ON i.user_id = u.id LEFT JOIN executors e ON i.executor_id = e.id;
-- 7. Агрегат: число инцидентов
SELECT COUNT(*) AS total FROM incidents;
-- 8. Агрегат: средний приоритет
SELECT AVG(priority) AS avg_priority, MAX(priority) AS max_priority FROM incidents;
-- 9. GROUP BY: количество по статусам
SELECT status, COUNT(*) AS total FROM incidents GROUP BY status;
-- 10. GROUP BY: количество по приоритетам
SELECT priority, COUNT(*) AS total FROM incidents GROUP BY priority;
-- 11. GROUP BY и JOIN: количество по авторам
SELECT u.name, COUNT(i.id) AS total FROM users u LEFT JOIN incidents i
ON i.user_id = u.id GROUP BY u.id, u.name;
-- 12. HAVING: статусы с количеством инцидентов не менее одного
SELECT status, COUNT(*) AS total FROM incidents GROUP BY status HAVING COUNT(*) >= 1;
-- 13. Многокритериальная фильтрация и сортировка
SELECT id, title FROM incidents WHERE priority >= 2 AND status != 'Закрыт' ORDER BY created_at DESC;
-- 14. LIMIT/OFFSET
SELECT id, title FROM incidents ORDER BY id LIMIT 10 OFFSET 0;
-- 15. Поиск без назначенного исполнителя: IS NULL
SELECT id, title FROM incidents WHERE executor_id IS NULL;
-- 16. Подзапрос: авторы без инцидентов
SELECT name FROM users WHERE id NOT IN (SELECT user_id FROM incidents);
