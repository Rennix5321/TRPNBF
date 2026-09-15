import pytest
from incidents import (add_incident, assign_executor, calculate_statistics,
                       filter_incidents, find_incidents,
                       update_incident_status)

def test_add_incident():
    items = []
    item = add_incident(items, "Сбой сети", "Нет связи", "Иван", 3)
    assert item["id"] == 1 and item["status"] == "Новый"

def test_find_incidents():
    items = []
    add_incident(items, "Сбой сети", "Нет связи", "Иван", 3)
    assert find_incidents(items, "СЕТИ")

def test_filter_incidents():
    items = []
    add_incident(items, "A", "Описание", "Иван", 1)
    add_incident(items, "B", "Описание", "Анна", 3)
    assert filter_incidents(items, "Новый", 3)[0]["title"] == "B"

def test_assign_executor():
    items = []
    add_incident(items, "Сбой", "Описание", "Иван", 2)
    assert assign_executor(items, 1, "Анна")["status"] == "В работе"

def test_unknown_incident():
    with pytest.raises(KeyError):
        update_incident_status([], 99, "Закрыт")

def test_statistics():
    items = []
    add_incident(items, "A", "Описание", "Иван", 1)
    add_incident(items, "B", "Описание", "Анна", 3, "Петр")
    assert calculate_statistics(items)["total"] == 2
