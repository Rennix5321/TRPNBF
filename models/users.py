"""Пользователи и исполнители системы."""


class User:
    """Пользователь, зарегистрировавший инцидент."""

    def __init__(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя пользователя не должно быть пустым")
        self._name = name.strip()

    @property
    def name(self) -> str:
        """Имя не меняется после создания объекта."""
        return self._name

    def __str__(self) -> str:
        return f"Пользователь: {self.name}"


class Executor(User):
    """Исполнитель наследует имя и проверку данных пользователя."""

    def __str__(self) -> str:
        return f"Исполнитель: {self.name}"
