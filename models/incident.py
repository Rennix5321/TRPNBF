"""Инцидент и операции над его состоянием."""
from datetime import datetime

from models.users import Executor, User

STATUSES = ("Новый", "В работе", "Решен", "Закрыт")
PRIORITIES = {1: "Низкий", 2: "Средний", 3: "Высокий"}


class Incident:
    """Инцидент хранит ссылки на автора и назначенного исполнителя."""

    def __init__(self, incident_id: int, title: str, description: str,
                 user: User, priority: int, executor: Executor | None = None,
                 created_at: str | None = None,
                 status: str | None = None) -> None:
        if type(incident_id) is not int or incident_id < 1:
            raise ValueError("ID должен быть положительным целым числом")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название обязательно")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Описание обязательно")
        if not isinstance(user, User):
            raise ValueError("Автор должен быть объектом User")
        if executor is not None and not isinstance(executor, Executor):
            raise ValueError("Исполнитель должен быть объектом Executor")
        if type(priority) is not int or priority not in PRIORITIES:
            raise ValueError("Приоритет должен быть от 1 до 3")
        if created_at is None:
            created_at = datetime.now().isoformat(timespec="seconds")
        if not isinstance(created_at, str):
            raise ValueError("Дата должна быть строкой ISO 8601")
        datetime.fromisoformat(created_at)
        self._id = incident_id
        self.title = title.strip()
        self.description = description.strip()
        self._user = user
        self.priority = priority
        self._created_at = created_at
        self._executor = executor
        self._status = "В работе" if executor else "Новый"
        if status is not None:
            self.change_status(status)

    @property
    def id(self) -> int:
        """Идентификатор неизменяем после создания."""
        return self._id

    @property
    def user(self) -> User:
        """Автор не меняется при назначении исполнителя."""
        return self._user

    @property
    def created_at(self) -> str:
        """Дата регистрации сохраняется на весь срок жизни инцидента."""
        return self._created_at

    @property
    def priority(self) -> int:
        """Получить приоритет."""
        return self._priority

    @priority.setter
    def priority(self, value: int) -> None:
        """Проверить приоритет до изменения состояния."""
        if type(value) is not int or value not in PRIORITIES:
            raise ValueError("Приоритет должен быть целым числом от 1 до 3")
        self._priority = value

    @property
    def status(self) -> str:
        """Статус доступен для чтения; меняется через проверяемый метод."""
        return self._status

    @property
    def executor(self) -> Executor | None:
        """Вернуть назначенного исполнителя."""
        return self._executor

    @property
    def priority_name(self) -> str:
        """Вернуть название приоритета."""
        return PRIORITIES[self.priority]

    def assign_executor(self, executor: Executor) -> None:
        """Назначить исполнителя и взять новый инцидент в работу."""
        if not isinstance(executor, Executor):
            raise ValueError("Нужен объект Executor")
        if self.status == "Закрыт":
            raise ValueError("Сначала откройте инцидент: статус В работе")
        self._executor = executor
        if self.status == "Новый":
            self._status = "В работе"

    def change_status(self, status: str) -> None:
        """Установить один из допустимых статусов ПР2."""
        if status not in STATUSES:
            raise ValueError(f"Допустимые статусы: {', '.join(STATUSES)}")
        if status == "Новый" and self.executor is not None:
            raise ValueError("Инцидент с исполнителем не может быть новым")
        if status != "Новый" and self.executor is None:
            raise ValueError("Сначала назначьте исполнителя")
        self._status = status

    def __str__(self) -> str:
        return (f"№{self.id}: {self.title} | {self.priority_name} | "
                f"{self.status}")
