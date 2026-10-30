## Запуск в Windows PowerShell

Требуется Python 3.10 или новее; для соответствия методичке рекомендуется 3.11.
Откройте PowerShell в корне репозитория, где находятся `manage.py` и `main.py`.
Команды ниже используют Python из окружения напрямую, активация не требуется.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Откройте http://127.0.0.1:8000/. Остановка сервера: Ctrl+C.
`migrate` готовит таблицы встроенных приложений Django (auth, sessions, admin).
Инциденты продолжают храниться в JSON; миграции не переносят их в базу.

Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py check
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Если окружение уже создано, начните с установки зависимостей.

## Реализованные страницы

| Адрес | Функция | Что показывает |
| --- | --- | --- |
| `/` | `homepage.views.index` | Описание системы и навигация |
| `/incidents/` | `web_incidents.views.incident_list` | Список инцидентов и ссылки на карточки |
| `/incidents/<int:incident_id>/` | `web_incidents.views.incident_detail` | ID, название, описание, автор, исполнитель, приоритет, статус, дата |
| `/statistics/` | `dashboard.views.statistics` | Количество инцидентов, распределение по статусам и приоритетам |
| Неизвестный адрес | `homepage.views.page_not_found` | Общая страница 404 при отключенной отладке |

Примеры: `/incidents/1/` - существующий инцидент;
`/incidents/999/` - маршрут найден, объект отсутствует;
`/incidents/abc/` и `/nonexistent/` - маршрут не найден.
Страница `/admin/` является встроенной административной страницей Django;
управление инцидентами через нее на ПР5 не реализовано.

## Структура и обработка запроса

- `manage.py` - команды проверки, миграций и запуска сервера.
- `incident_site/` - конфигурационный пакет: settings, корневой URLconf, ASGI/WSGI.
- `homepage/` - главная, общий HTML-каркас `page(title, content)`, handler404.
- `web_incidents/` - список и карточка инцидента, собственный urls.py.
- `dashboard/` - страница статистики, собственный urls.py.
- `models/` - обычные классы ПР3: `Incident`, `User`, `Executor`.
- `incidents.py` - операции над объектами, поиск, фильтрация и статистика.
- `storage.py` - проверка JSON, загрузка объектов, атомарное сохранение.
- `data/incidents.json` - данные консольной и веб-версии.
- `main.py`, `utils.py` - сохраненная консольная версия.
- `tests/` - проверки ПР3 и HTTP-проверки ПР5.
- `docs/DEFENSE_PR5.md` - ответы и демонстрация всех 25 пунктов защиты.
- `docs/PR3.md` - документация предыдущего этапа.

Запрос `/incidents/1/` проходит через `incident_site/urls.py`, затем
`web_incidents/urls.py`. Конвертер `int` передает `incident_id=1` в
`incident_detail(request, incident_id)`. Представление вызывает
`load_incidents(settings.INCIDENTS_FILE)`, затем `find_incident_by_id()`.
Атрибуты полученного объекта вставляются в HTML и передаются в `page()`.
`HttpResponse` отправляет страницу и HTTP-статус браузеру.
При отсутствии объекта возвращается отдельный ответ со статусом 404.



## HTML, CSS и Bootstrap

На этапе ПР5 HTML формируется Python-строками, как в задании.
`homepage.views.page()` создает общие head, навигацию, main и footer.
Отдельные views передают заголовок вкладки и разметку содержимого.
Bootstrap 5.3.3 подключен через CDN: для полной загрузки стилей нужен интернет.
Используются `container`, `display-4`, `lead`, `btn`, `card`, `badge`,
`list-group`, `row`, `col-md-6`. Дополнительный CSS задает фон, навигацию
и отображение многострочного описания. Текстовые данные JSON экранируются
через `escape()`, чтобы разметка из названия или описания не выполнялась.

## Данные и сохранение ПР3

`load_incidents()` создает `list[Incident]`, восстанавливает `User` и `Executor`.
`find_incident_by_id()` возвращает объект или `None`; старый `get_incident()`
по-прежнему вызывает `KeyError` для отсутствующего ID, сохраняя контракт ПР3.
`calculate_statistics()` используется и консолью, и страницей статистики.
Путь JSON определяется относительно проекта, а не текущей папки терминала.
Изменения JSON видны при обновлении страницы, перезапуск сервера не требуется.

Консольный запуск:

```powershell
.\.venv\Scripts\python.exe main.py
```

Все функции ПР3 сохранены: создание, поиск, фильтры, сортировка, назначение
исполнителя, смена статуса, статистика и сохранение в JSON. Веб-версия ПР5
предназначена для просмотра. Создание и изменение через формы, шаблоны,
вход пользователей и перенос предметных классов в Django ORM - следующие этапы.

## Проверка 404 и настройки

По умолчанию `DEBUG=True`. Для показа собственной страницы 404 перед защитой
остановите сервер и выполните в том же окне PowerShell:

```powershell
$env:DJANGO_DEBUG = "False"
.\.venv\Scripts\python.exe manage.py runserver
```

Проверьте `/nonexistent/`, `/incidents/abc/` и `/incidents/999/`.
`handler404` обрабатывает первые два адреса. Отсутствующий объект обрабатывается
явным `HttpResponse(..., status=404)` внутри `incident_detail()`.
Прямой возврат ответа 404 сам по себе не вызывает handler404.

Возврат к отладке после остановки сервера:

```powershell
Remove-Item Env:DJANGO_DEBUG
```

`ALLOWED_HOSTS` содержит localhost, 127.0.0.1 и локальный IPv6.
Это конфигурация для учебного локального запуска. При дальнейшем размещении
на сервере нужно указать настоящий домен и задать отдельный `DJANGO_SECRET_KEY`.

## Автоматические проверки

```powershell
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m flake8 .
.\.venv\Scripts\python.exe manage.py check
```

67 тестов: 51 исходный тест ПР3 и 16 HTTP/интеграционных проверок ПР5.
Веб-тесты проверяют страницы, именованные маршруты, числовой конвертер,
отсутствующий объект, handler404, DEBUG, ALLOWED_HOSTS, обновление JSON,
экранирование текста, пустые данные и отсутствие записи при просмотре.
Тесты работают с временными файлами и не меняют `data/incidents.json`.

## Подготовка к защите

Читайте [все 25 пунктов и план демонстрации](docs/DEFENSE_PR5.md).
Таблица из методички адаптирована к предметной области инцидентов.
Коммиты этапа отмечены префиксом `PR5:`; перед добавлением Django создана
отдельная контрольная точка. Задания Яндекс Практикума и личные скриншоты
прохождения курса выполняются отдельно от доработки репозитория.

## ПР6 — шаблоны Django

Веб-представления перенесены на `render()` и Django Templates. Общий каркас —
`templates/base.html`, страницы находятся в `homepage/templates/homepage/`,
`web_incidents/templates/web_incidents/`, `dashboard/templates/dashboard/`.
Используются `extends`, `block`, `include`, `for`/`empty`, `if`, фильтры,
контекст, пространства имён URL. Файлы CSS, JS и логотип —
`homepage/static/homepage/`. Прежняя функция `page()` оставлена только ради
совместимости с историческими тестами; web views ею не пользуются.
JSON-хранилище и консольная реализация прежних работ сохранены.

## ПР7 — SQLite и SQL (без Django ORM)

Схема — `sql/schema.sql`, 16 учебных SQL-запросов — `sql/queries.sql`,
подключение — `db/database.py`, перенос данных — `db/import_json.py`.
База `data/incidents.sqlite` хранит `users`, `executors`, `incidents`.
В `incidents` определены внешние ключи `user_id` и необязательный
`executor_id`; в Python включается `PRAGMA foreign_keys = ON`.
Используются `executemany`, `commit`, `sqlite3.Row`, `?` для параметров.

Для повторного импорта с заменой данных SQLite из JSON:

```bash
python -m db.import_json
```

| Адрес | Источник и назначение |
|---|---|
| `/` | Главная страница Django |
| `/incidents/` | Исходные объекты `Incident` из JSON |
| `/incidents/1/` | Карточка объекта, ID и 404 |
| `/statistics/` | Исходная статистика по JSON |
| `/incidents/sql/` | Список из SQLite через `SELECT` и `JOIN` |
| `/incidents/search/?status=Решен&priority=3` | SQL-поиск по параметрам |
| `/statistics/sql/` | `COUNT`, `GROUP BY` и `JOIN` из SQLite |

Запуск (в корне проекта):

```bash
python -m pip install -r requirements.txt
python -m db.import_json
python manage.py check
python manage.py runserver
pytest -v
flake8 . --extend-exclude=venv
```

Запросы БД исполняются через стандартный `sqlite3`, не через ORM.
После изменения JSON следует повторить импорт, чтобы обновить данные SQLite.
Скрипт импорта заменяет имеющиеся записи; не запускайте его, если в базе
есть самостоятельные изменения, которые нужно сохранить.

На защите можно открыть `data/incidents.sqlite` через расширение SQLite Viewer,
показать SQL из `sql/queries.sql`, затем пройти сценарии из
`docs/DEFENSE_PR6_PR7.md`. Статус проверки и Git-коммиты следует показать
на компьютере после установки зависимостей и фиксации изменений в Git.


## ПР9 — Django ORM, связи и миграции

Ранее реализованные консольная версия, JSON и файлы SQL ПР7 сохранены для сравнения.
Веб-страницы `/incidents/sql/`, `/incidents/search/`, `/statistics/sql/` теперь используют Django ORM, а `/incidents/<id>/` получает объект через ORM. `/incidents/` и `/statistics/` оставлены как исторические JSON-страницы.

**Начальная настройка:**

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py import_pr7
python manage.py check
python manage.py runserver
```

`migrate` создаёт таблицы ORM в `db.sqlite3`, `import_pr7` переносит записи из `data/incidents.sqlite` (источник ПР7). Команда импорта повторно запускается без дублирования записей, обновляя совпадающие ID. Не следует повторно выполнять `python -m db.import_json` после изменения исходных данных только в ORM: старый импорт пересоздаёт источник ПР7 из JSON.

Модели и связи: `web_incidents/models.py` (Incident, IncidentUser, Executor); миграция — `web_incidents/migrations/0001_initial.py`; управление переносом — `web_incidents/management/commands/import_pr7.py`.

**Возможности ORM:** детальная страница, поиск по названию/описанию и автору, фильтрация по статусу и приоритету, безопасная сортировка, постраничный вывод, агрегирование по статусам, приоритетам и авторам. Примеры более 15 ORM-выражений находятся в `web_incidents/orm_examples.py`. CRUD можно показать через `python manage.py shell` или Django admin (для последней нужен суперпользователь).

**Проверки:** `python manage.py check`, `python manage.py makemigrations --check --dry-run`, `pytest -v`, `flake8 . --extend-exclude=venv`. Для нового теста используется pytest-django.


