"""Сквозные сценарии меню с отдельными временными данными."""
import json
from pathlib import Path

import main


def enter(monkeypatch, answers: list[str]) -> None:
    """Подставить последовательность ответов вместо ручного ввода."""
    iterator = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _: next(iterator))


def test_full_workflow(tmp_path, monkeypatch, capsys):
    file = tmp_path / "incidents.json"
    enter(monkeypatch, [
        "2", "Сбой сети", "Нет связи", "Иван", "abc", "4", "3",
        "5", "1", "Анна", "6", "1", "Решен", "6", "1", "Закрыт",
        "3", "СЕТИ", "4", "Закрыт", "3", "8", "7", "9", "1",
        "6", "99", "0"])
    main.main(file)
    text = capsys.readouterr().out
    row = json.loads(file.read_text(encoding="utf-8"))[0]
    assert row["status"] == "Закрыт"
    assert row["executor"] == "Анна"
    assert row["user"] == "Иван"
    assert "не найден" in text
    assert "Всего: 1" in text
    assert "Изменения сохранены" in text
    enter(monkeypatch, ["1", "0"])
    main.main(file)
    assert "Сбой сети" in capsys.readouterr().out


def test_failed_save_rolls_back_memory(tmp_path, monkeypatch, capsys):
    file = tmp_path / "incidents.json"
    original_save = main.save_incidents
    attempts = 0

    def fail_once(path: Path, items: list) -> None:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise OSError("Нет доступа")
        original_save(path, items)

    monkeypatch.setattr(main, "save_incidents", fail_once)
    enter(monkeypatch, ["2", "Сбой", "Описание", "Иван", "3", "7", "0"])
    main.main(file)
    text = capsys.readouterr().out
    assert "Всего: 0" in text
    assert "Изменения сохранены" not in text
    assert json.loads(file.read_text(encoding="utf-8")) == []


def test_bad_file_stops_before_menu(tmp_path, capsys):
    file = tmp_path / "incidents.json"
    file.write_text("{broken", encoding="utf-8")
    main.main(file)
    text = capsys.readouterr().out
    assert "Ошибка загрузки" in text
    assert "Выберите" not in text
    assert file.read_text() == "{broken"


def test_invalid_actions_do_not_change_record(tmp_path, monkeypatch, capsys):
    file = tmp_path / "incidents.json"
    enter(monkeypatch, [
        "2", "Сбой", "Описание", "Иван", "2",
        "6", "1", "Закрыт", "4", "", "abc", "4", "", "4", "100", "0"])
    main.main(file)
    assert json.loads(file.read_text(encoding="utf-8"))[0]["status"] == "Новый"
    assert "Ошибка" in capsys.readouterr().out


def test_failed_assignment_rolls_back_nested_data(tmp_path, monkeypatch):
    file = tmp_path / "incidents.json"
    enter(monkeypatch, ["2", "Сбой", "Описание", "Иван", "3", "0"])
    main.main(file)
    original_save = main.save_incidents
    attempts = 0

    def fail_once(path: Path, items: list) -> None:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise OSError("Нет доступа")
        original_save(path, items)

    monkeypatch.setattr(main, "save_incidents", fail_once)
    enter(monkeypatch, ["5", "1", "Анна", "0"])
    main.main(file)
    row = json.loads(file.read_text(encoding="utf-8"))[0]
    assert row["executor"] is None
    assert row["status"] == "Новый"
