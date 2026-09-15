"""Точка запуска консольной системы учета инцидентов."""
from pathlib import Path
from incidents import (add_incident, assign_executor, calculate_statistics,
                       filter_incidents, find_incidents, get_priority_name,
                       sort_incidents, update_incident_status)
from storage import load_incidents, save_incidents
from utils import input_int

DATA_FILE = Path(__file__).parent / "data" / "incidents.json"

def show_incidents(incidents: list[dict]) -> None:
    """Вывести список инцидентов."""
    if not incidents:
        print("Инциденты не найдены.")
        return
    print("\nID | Приоритет | Статус     | Название")
    print("-" * 66)
    for item in incidents:
        print(f"{item['id']:>2} | {get_priority_name(item['priority']):<9} | "
              f"{item['status']:<10} | {item['title']}")

def register_incident(incidents: list[dict]) -> None:
    """Запросить данные и зарегистрировать инцидент."""
    item = add_incident(
        incidents, input("Название: "), input("Описание: "),
        input("Пользователь: "),
        input_int("Приоритет (1-3): ", 1, 3))
    print(f"Инцидент №{item['id']} зарегистрирован.")

def print_statistics(incidents: list[dict]) -> None:
    """Вывести статистику."""
    stats = calculate_statistics(incidents)
    print(f"Всего: {stats['total']}")
    for group_name in ("by_status", "by_priority"):
        for name, count in stats[group_name].items():
            print(f"  {name}: {count}")

def print_menu() -> None:
    """Вывести меню."""
    print("\n=== Система учета инцидентов ===")
    print("1. Показать все  2. Зарегистрировать  3. Найти")
    print("4. Фильтровать   5. Назначить        6. Изменить статус")
    print("7. Статистика    8. Сортировка       0. Выход")

def main() -> None:
    """Выполнять команды меню до выхода."""
    incidents = load_incidents(DATA_FILE)
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "1":
                show_incidents(incidents)
            elif choice == "2":
                register_incident(incidents)
                save_incidents(DATA_FILE, incidents)
            elif choice == "3":
                show_incidents(find_incidents(incidents, input("Поиск: ")))
            elif choice == "4":
                status = input("Статус (Enter - любой): ").strip() or None
                text = input("Приоритет 1-3 (Enter - любой): ").strip()
                show_incidents(filter_incidents(
                    incidents, status, int(text) if text else None))
            elif choice == "5":
                assign_executor(incidents, input_int("ID: ", 1),
                                input("Исполнитель: "))
                save_incidents(DATA_FILE, incidents)
            elif choice == "6":
                update_incident_status(incidents, input_int("ID: ", 1),
                                       input("Новый статус: ").strip())
                save_incidents(DATA_FILE, incidents)
            elif choice == "7":
                print_statistics(incidents)
            elif choice == "8":
                show_incidents(sort_incidents(
                    incidents, "priority", reverse=True))
            elif choice == "0":
                save_incidents(DATA_FILE, incidents)
                print("Данные сохранены.")
                break
            else:
                print("Неизвестная команда.")
        except (ValueError, KeyError) as error:
            print(f"Ошибка: {error}")

if __name__ == "__main__":
    main()
