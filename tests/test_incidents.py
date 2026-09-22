"""Проверки объектной модели и функций ПР2 после адаптации."""
import pytest

from incidents import (add_incident, calculate_statistics, filter_incidents,
                       find_incidents, get_incident, sort_incidents)
from models import Executor, Incident, User


@pytest.fixture
def items() -> list[Incident]:
    user = User("Иван")
    result = []
    add_incident(result, "Сбой сети", "Нет связи", user, 3)
    add_incident(result, "Принтер", "Нет бумаги", user, 1)
    return result


def test_add_incident(items):
    assert [item.id for item in items] == [1, 2]
    assert items[0].status == "Новый"
    assert items[0].user is items[1].user


def test_find_incidents(items):
    assert find_incidents(items, "СЕТИ") == [items[0]]
    assert find_incidents(items, "БУМАГИ") == [items[1]]


def test_filter_incidents(items):
    assert filter_incidents(items, "Новый", 3) == [items[0]]


def test_assign_executor(items):
    executor = Executor("Анна")
    items[0].assign_executor(executor)
    assert items[0].executor is executor
    assert items[0].status == "В работе"


def test_status_change(items):
    items[0].assign_executor(Executor("Анна"))
    items[0].change_status("Закрыт")
    assert items[0].status == "Закрыт"
    with pytest.raises(ValueError):
        items[0].change_status("ошибка")
    assert items[0].status == "Закрыт"


def test_encapsulation(items):
    with pytest.raises(AttributeError):
        items[0].status = "ошибка"


def test_unknown_incident():
    with pytest.raises(KeyError):
        get_incident([], 99)


def test_statistics(items):
    assert calculate_statistics(items) == {
        "total": 2,
        "by_status": {"Новый": 2, "В работе": 0, "Решен": 0, "Закрыт": 0},
        "by_priority": {"Низкий": 1, "Средний": 0, "Высокий": 1}}


def test_sort_incidents(items):
    assert sort_incidents(items, "priority") == [items[1], items[0]]
    assert items[0].priority == 3


def test_string_representation(items):
    assert "Сбой сети" in str(items[0])
    assert str(User("Иван")) == "Пользователь: Иван"
    assert str(Executor("Анна")) == "Исполнитель: Анна"
    assert isinstance(Executor("Анна"), User)


@pytest.mark.parametrize("priority", [0, 4, True, "3"])
def test_invalid_priority(priority):
    with pytest.raises(ValueError):
        Incident(1, "Сбой", "Описание", User("Иван"), priority)


def test_empty_name():
    with pytest.raises(ValueError):
        User("   ")


def test_empty_statistics():
    assert calculate_statistics([])["total"] == 0


def test_cannot_close_without_executor(items):
    with pytest.raises(ValueError, match="назначьте"):
        items[0].change_status("Закрыт")
    assert items[0].status == "Новый"


def test_cannot_make_assigned_incident_new(items):
    items[0].assign_executor(Executor("Анна"))
    with pytest.raises(ValueError):
        items[0].change_status("Новый")
    assert items[0].status == "В работе"


def test_closed_incident_requires_reopening(items):
    anna = Executor("Анна")
    items[0].assign_executor(anna)
    items[0].change_status("Закрыт")
    with pytest.raises(ValueError):
        items[0].assign_executor(Executor("Петр"))
    assert items[0].executor is anna
    items[0].change_status("В работе")
    items[0].assign_executor(Executor("Петр"))
    assert items[0].executor.name == "Петр"


def test_invalid_priority_assignment_preserves_value(items):
    with pytest.raises(ValueError):
        items[0].priority = 99
    assert items[0].priority == 3


def test_bool_filter_rejected(items):
    with pytest.raises(ValueError):
        filter_incidents(items, priority=True)


def test_id_is_readonly(items):
    with pytest.raises(AttributeError):
        items[0].id = 2


def test_author_is_not_executor(items):
    author = items[0].user
    items[0].assign_executor(Executor("Анна"))
    assert items[0].user is author


def test_initial_state_with_executor():
    item = Incident(1, "Сбой", "Описание", User("Иван"), 2,
                    Executor("Анна"))
    assert item.status == "В работе"
