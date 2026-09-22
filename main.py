"""Консольное меню системы учета инцидентов."""
import argparse
from copy import deepcopy
from pathlib import Path

from incidents import (add_incident, calculate_statistics, filter_incidents,
                       find_incidents, get_incident, sort_incidents)
from models import Executor, Incident, User
from storage import load_incidents, save_incidents
from utils import input_int

DATA_FILE = Path(__file__).parent / "data" / "incidents.json"


def show_incidents(incidents: list[Incident]) -> None:
    """Показать список с автором и исполнителем."""
    if not incidents:
        print("Инциденты не найдены.")
        return
    print("ID | Приоритет | Статус | Пользователь | Исполнитель | Название")
    for item in incidents:
        executor = item.executor.name if item.executor else "не назначен"
        print(f"{item.id} | {item.priority_name} | {item.status} | "
              f"{item.user.name} | {executor} | {item.title}")


def register_incident(incidents: list[Incident]) -> None:
    """Ввести данные и добавить инцидент в рабочую копию коллекции."""
    title = input("Название: ")
    description = input("Описание: ")
    user = User(input("Пользователь: "))
    priority = input_int("Приоритет (1-3): ", 1, 3)
    add_incident(incidents, title, description, user, priority)


def show_details(item: Incident) -> None:
    """Показать полную карточку и строковые представления объектов."""
    print(item)
    print(item.description)
    print(item.user)
    print(item.executor or "Исполнитель не назначен")
    print(f"Дата: {item.created_at}")


def print_statistics(incidents: list[Incident]) -> None:
    """Показать полную статистику, включая нулевые группы."""
    stats = calculate_statistics(incidents)
    print(f"Всего: {stats['total']}")
    for group, title in (("by_status", "По статусам"),
                         ("by_priority", "По приоритетам")):
        print(title)
        for name, count in stats[group].items():
            print(f"  {name}: {count}")


def print_menu() -> None:
    """Вывести команды меню."""
    print("\n=== Система учета инцидентов ===")
    print("1. Показать все  2. Зарегистрировать  3. Найти")
    print("4. Фильтровать   5. Назначить        6. Изменить статус")
    print("7. Статистика    8. Сортировка       9. Карточка")
    print("0. Сохранить и выйти")


def main(filename: Path | None = None) -> None:
    """Изменять данные в памяти только после успешного сохранения."""
    path = filename if filename is not None else DATA_FILE
    try:
        incidents = load_incidents(path)
    except (ValueError, OSError) as error:
        print(f"Ошибка загрузки: {error}")
        return
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        try:
            if choice in {"2", "5", "6"}:
                candidate = deepcopy(incidents)
                if choice == "2":
                    register_incident(candidate)
                else:
                    item = get_incident(candidate, input_int("ID: ", 1))
                    if choice == "5":
                        item.assign_executor(Executor(input("Исполнитель: ")))
                    else:
                        print("Статусы: Новый, В работе, Решен, Закрыт")
                        item.change_status(input("Новый статус: ").strip())
                save_incidents(path, candidate)
                incidents = candidate
                print("Изменения сохранены.")
            elif choice == "1":
                show_incidents(incidents)
            elif choice == "3":
                show_incidents(find_incidents(incidents, input("Поиск: ")))
            elif choice == "4":
                status = input("Статус (Enter - любой): ").strip() or None
                text = input("Приоритет 1-3 (Enter - любой): ").strip()
                show_incidents(filter_incidents(
                    incidents, status, int(text) if text else None))
            elif choice == "7":
                print_statistics(incidents)
            elif choice == "8":
                show_incidents(sort_incidents(
                    incidents, "priority", reverse=True))
            elif choice == "9":
                show_details(get_incident(incidents, input_int("ID: ", 1)))
            elif choice == "0":
                save_incidents(path, incidents)
                print("Данные сохранены.")
                return
            else:
                print("Неизвестная команда.")
        except (ValueError, KeyError, OSError) as error:
            print(f"Ошибка: {error}. Изменения не применены.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Учет инцидентов")
    parser.add_argument("--data", type=Path, default=DATA_FILE,
                        help="Отдельный JSON для демонстрации")
    try:
        main(parser.parse_args().data)
    except (EOFError, KeyboardInterrupt):
        print("\nРабота прервана. Завершенные операции сохранены.")
