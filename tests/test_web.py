"""Проверки HTTP, маршрутов и интеграции веб-слоя с объектами ПР3."""
import json
import os

import django
import pytest
from django.test import Client, override_settings
from django.urls import Resolver404, resolve, reverse

from incidents import find_incident_by_id
from storage import load_incidents

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "incident_site.settings")
django.setup()


@pytest.fixture
def data_file(tmp_path):
    row = {
        "id": 1, "title": "Сбой сети", "description": "Нет связи",
        "user": "Иван", "executor": None, "priority": 3,
        "status": "Новый", "created_at": "2026-09-15T09:00:00",
    }
    file = tmp_path / "incidents.json"
    file.write_text(json.dumps([row], ensure_ascii=False), encoding="utf-8")
    return file


@pytest.fixture
def client(data_file):
    with override_settings(INCIDENTS_FILE=data_file,
                           ALLOWED_HOSTS=["testserver"], DEBUG=False):
        yield Client()


@pytest.mark.parametrize("url,text", [
    ("/", "Система учета инцидентов"),
    ("/incidents/", "Сбой сети"),
    ("/incidents/1/", "Не назначен"),
    ("/statistics/", "Всего инцидентов: 1"),
])
def test_pages(client, url, text):
    response = client.get(url)
    assert response.status_code == 200
    assert response["Content-Type"] == "text/html; charset=utf-8"
    html = response.content.decode()
    assert text in html
    assert '<html lang="ru">' in html
    assert 'bootstrap@5.3.3' in html
    assert 'href="/incidents/"' in html
    assert 'href="/statistics/"' in html


def test_numeric_route_and_named_reverse():
    match = resolve("/incidents/999/")
    assert match.view_name == "web_incidents:incident_detail"
    assert match.kwargs == {"incident_id": 999}
    assert type(match.kwargs["incident_id"]) is int
    assert reverse(match.view_name, args=[999]) == "/incidents/999/"
    with pytest.raises(Resolver404):
        resolve("/incidents/abc/")


@pytest.mark.parametrize("url", ["/nonexistent/", "/incidents/abc/"])
def test_unmatched_route_custom_404(client, url):
    response = client.get(url)
    assert response.status_code == 404
    assert "404 - страница не найдена" in response.content.decode()


def test_missing_incident_uses_explicit_response(client):
    response = client.get("/incidents/999/")
    assert response.status_code == 404
    html = response.content.decode()
    assert "Инцидент не найден" in html
    assert "404 - страница не найдена" not in html


def test_debug_uses_technical_404(client):
    with override_settings(DEBUG=True):
        response = client.get("/nonexistent/")
    assert response.status_code == 404
    assert "incident_site.urls" in response.content.decode()


def test_host_validation(client):
    response = client.get("/", HTTP_HOST="untrusted.example")
    assert response.status_code == 400


def test_domain_search_returns_object_or_none(data_file):
    items = load_incidents(data_file)
    assert find_incident_by_id(items, 1) is items[0]
    assert find_incident_by_id(items, 999) is None


def test_detail_reflects_updated_json_and_object_links(client, data_file):
    row = json.loads(data_file.read_text(encoding="utf-8"))[0]
    row.update(title="Новый заголовок", user="Мария", executor="Анна",
               status="В работе", priority=1)
    data_file.write_text(json.dumps([row]), encoding="utf-8")
    html = client.get("/incidents/1/").content.decode()
    for value in ["Новый заголовок", "Мария", "Анна", "В работе", "Низкий"]:
        assert value in html
    assert "Низкий: 1" in client.get("/statistics/").content.decode()


def test_json_text_is_escaped(client, data_file):
    row = json.loads(data_file.read_text(encoding="utf-8"))[0]
    row.update(title='<script>alert("x")</script>',
               description="<img src=x onerror=alert(1)>",
               user="<b>Иван</b>", executor="<b>Анна</b>", status="В работе")
    data_file.write_text(json.dumps([row]), encoding="utf-8")
    for url in ["/incidents/", "/incidents/1/"]:
        html = client.get(url).content.decode()
        assert "<script>" not in html
        assert "&lt;script&gt;" in html
    html = client.get("/incidents/1/").content.decode()
    assert "<img src=x" not in html
    assert "<b>Иван</b>" not in html
    assert "<b>Анна</b>" not in html


def test_empty_data(client, data_file):
    data_file.write_text("[]", encoding="utf-8")
    assert "пока отсутствуют" in client.get("/incidents/").content.decode()
    assert "Всего инцидентов: 0" in client.get("/statistics/").content.decode()
    assert client.get("/incidents/1/").status_code == 404


def test_browsing_does_not_change_json(client, data_file):
    original = data_file.read_bytes()
    for url in ["/", "/incidents/", "/incidents/1/", "/statistics/",
                "/incidents/999/", "/nonexistent/"]:
        client.get(url)
    assert data_file.read_bytes() == original


def test_shared_page_title_is_escaped():
    from homepage.views import page
    html = page("<b>Заголовок</b>", "<h1>Содержимое</h1>")
    assert "<title>&lt;b&gt;Заголовок&lt;/b&gt;</title>" in html
    assert "<h1>Содержимое</h1>" in html
