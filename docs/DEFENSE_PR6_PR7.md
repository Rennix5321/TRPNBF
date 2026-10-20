# Защита ПР6 и ПР7 — 50 показателей

Запуск: `python -m pip install -r requirements.txt`, `python -m db.import_json`, `python manage.py runserver`.
Требования адаптированы с учебного Roomly на систему учёта инцидентов.

## ПР6. Шаблоны Django

1. **Наследование.** `templates/base.html` и `homepage/templates/homepage/index.html`: `extends`. Поменять дочерний `block title`, обновить браузер — заголовок вкладки изменится.
2. **Блоки.** `base.html`: `block title/content`; `index.html`: их реализация. Изменить текст в `block content` и обновить `/`.
3. **Контекст.** `web_incidents/views.py` → `incident_list`: ключ `incidents` передаётся в `incident_list.html`. Переименовать только во view — цикл не получит список. Вернуть.
4. **Атрибуты.** `incident_detail.html`: `incident.title`, `incident.priority_name`. Несуществующий атрибут обычно даёт пустую строку, поэтому легко пропустить опечатку.
5. **Несуществующая переменная.** Попробовать `{{ missing_value }}` в шаблоне; по умолчанию пустая строка (если не перенастроен `string_if_invalid`). Удалить опытную строку.
6. **Автоэкранирование.** `tests/test_web.py::test_json_text_is_escaped`: тег `<script>` в названии выводится как текст, а не выполняется. `safe` нельзя использовать с недоверенным вводом.
7. **Коллекция.** `incident_list.html`: `for/empty`, заменить JSON в тестовом файле на `[]` и убедиться, что показан текст о пустом списке.
8. **Условие.** `incident_detail.html`: `if incident.status == 'Закрыт'`; изменить на другую проверку — изменится оформление статуса.
9. **Фильтры.** `incident_card.html`: `default`. Добавить `|upper` к `incident.title` и показать изменение регистра; убрать.
10. **Пустые значения.** `incident_detail.html`: `incident.executor.name|default:"Не назначен"`. Продемонстрировать запись без исполнителя в тесте.
11. **Include.** `incident_list.html` включает `includes/incident_card.html`; изменение класса карточки меняет все элементы списка.
12. **Контекст include.** В цикле переменная `incident` передаётся подключаемому фрагменту. Изменение имени только в одном месте скрывает ожидаемые данные.
13. **Динамический URL.** `incident_card.html`: `{% url 'web_incidents:incident_detail' incident.id %}`; замените `id` на другое существующее число и проверьте href.
14. **Namespace.** `web_incidents/urls.py`: `app_name = 'web_incidents'`. Ссылки с тем же префиксом должны совпадать; переименование без правок ссылок даёт `NoReverseMatch`.
15. **int-конвертер.** `web_incidents/urls.py`: `<int:incident_id>`. `/incidents/abc/` не совпадает с маршрутом и даёт 404.
16. **Не найден объект.** `/incidents/999/`: `find_incident_by_id` вернёт `None`; view отдаст шаблон `incident_missing.html`, статус 404.
17. **Типы 404.** `/nonsense/` не проходит URLconf; `/incidents/999/` проходит маршрут, но объект отсутствует. Обе ошибки дают HTTP 404 на разных этапах.
18. **Не найден шаблон.** Неверный путь в `render()` приводит к `TemplateDoesNotExist`; ошибка синтаксиса внутри найденного файла — `TemplateSyntaxError`. Исправить и вернуть путь.
19. **Структура тегов.** Временно убрать `endfor` из `incident_list.html`, увидеть `TemplateSyntaxError`, восстановить закрывающий тег.
20. **Static.** `base.html`: `{% load static %}`, CSS и JS; `nav.html`: `logo.svg`. Неверный путь приводит к 404 ресурса в Network браузера.
21. **CSS.** `homepage/static/homepage/css/style.css`: изменить `.incident-card {border-left: ...}` и обновить `/incidents/`.
22. **JS.** `homepage/static/homepage/js/main.js`: он добавляет `title` для `.incident-card`; проверить загруженный файл в Network и сообщения Console.
23. **Каталоги.** `homepage/templates/homepage/`, `web_incidents/templates/web_incidents/`, `dashboard/templates/dashboard/` предотвращают конфликт одинаковых имён. `render(request, 'web_incidents/incident_list.html', ...)`.
24. **Связь view/template.** `incident_detail` передаёт ключ `incident`; `incident_detail.html` читает его поля. Изменение только одного имени создаёт пропуск; вернуть оба к одному имени.
25. **Полный HTTP путь.** `/incidents/1/` → `incident_site/urls.py` → `web_incidents/urls.py` → `incident_detail(request, incident_id)` → JSON `Incident` → context → шаблон + base → HTML. При отсутствии ID — 404 в view.

## ПР7. SQLite и SQL

1. **Структура.** `sql/schema.sql` + `data/incidents.sqlite`: `users` (авторы), `executors` (исполнители), `incidents` (обращения).
2. **Ключи.** `incidents.id INTEGER PRIMARY KEY`, внешние ключи `user_id` и `executor_id` в `schema.sql`; внешний ключ защищает ссылочную целостность при включённом PRAGMA.
3. **Создание схемы.** `db/import_json.py` исполняет `schema.sql` с `CREATE TABLE IF NOT EXISTS`, поэтому повторный запуск возможен. Импорт пересоздаёт записи, не таблицы.
4. **Подключение.** `db/database.py`: `sqlite3.connect(DB_PATH)`. Покажите `DB_PATH` и `SELECT COUNT(*) FROM incidents`.
5. **JSON → SQLite.** `db/import_json.py`: сначала авторы и исполнители, потом инциденты, так как последние ссылаются на них.
6. **Проверка импорта.** Сравнить JSON `len(...)` с `SELECT COUNT(*) FROM incidents`; показать содержимое в SQLite Viewer.
7. **SELECT.** `sql/queries.sql` запросы №1–2: выбрать все или отдельные столбцы.
8. **WHERE.** Запрос №3: `priority >= 3`; изменить порог на `2` — число результатов изменится.
9. **Фильтр статуса.** Запрос №4: `status IN ('Новый','В работе')`; заменить на `status = 'Решен'`.
10. **JOIN.** Запросы №5–6: `JOIN users ON i.user_id = u.id`, `LEFT JOIN executors` сохраняет записи без исполнителя.
11. **Несколько условий.** Запрос №13: `priority >= 2 AND status != 'Закрыт'`; поменять границу приоритета.
12. **COUNT.** Запрос №7: `COUNT(*)`; при пустой таблице возвращает `0`.
13. **GROUP BY.** Запросы №9–11: группировка по статусу, приоритету, авторам.
14. **HAVING.** Запрос №12: `HAVING COUNT(*) >= 1` отбирает группы, тогда как `WHERE` отбирает строки до группировки.
15. **Параметры.** `web_incidents/views.py::sql_search`: плейсхолдеры `?`, значения в `params`. Никогда не интерполировать ввод в SQL.
16. **SQLite Row.** `db/database.py`: `row_factory = sqlite3.Row`, далее `dict(row)`, доступ по названию (`item.title` в Django Template).
17. **Список из SQLite.** `/incidents/sql/` → `sql_incident_list` → SELECT + JOIN → `sql_list.html`.
18. **Фильтрация на странице.** `/incidents/search/?status=Решен` выдаёт только статус «Решен».
19. **Связанные данные.** `/incidents/sql/` показывает названия авторов и исполнителей, полученные из JOIN.
20. **Поиск по вводу.** `/incidents/search/?q=сервер&priority=3` → `GET` → параметры к SQL → HTML.
21. **Агрегаты.** `/statistics/sql/` → `COUNT(*)`, `GROUP BY status/priority`, статистика по авторам.
22. **Ключ контекста.** `sql_incident_list` передаёт `incidents`; `includes/sql_table.html` перебирает `incidents`. Имена должны совпадать.
23. **Пустой результат.** `/incidents/search/?q=нет-такой-строки` → `{% empty %}` «Записи не найдены», без SQL-ошибки.
24. **Ошибка SQL.** Временно заменить `i.status` на `i.unknown` в запросе, будет `sqlite3.OperationalError` (несуществующий столбец); восстановить.
25. **Полный запрос.** `/incidents/search/?status=Решен` → URLconf → `sql_search` → `GET` → безопасный `WHERE i.status = ?` → `sqlite3.Row` → контекст → `sql_search.html` + `sql_table.html` → браузер.

**Внимание.** Перед защитой обязательно установите зависимости, запустите `python manage.py check`, `pytest -v`, `flake8 . --extend-exclude=venv` и зафиксируйте изменения коммитами с `PR6:` и `PR7:` в своём Git-репозитории. Прохождение заданий Яндекс Практикума требует личного доступа; оно не подтверждается исходным кодом.
