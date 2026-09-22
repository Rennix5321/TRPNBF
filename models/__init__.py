"""Основные сущности системы учета инцидентов."""
from .incident import Incident
from .users import Executor, User

__all__ = ["Incident", "Executor", "User"]
