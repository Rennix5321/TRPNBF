"""Функции безопасного ввода."""

def input_int(prompt: str, minimum: int | None = None,
              maximum: int | None = None) -> int:
    """Запрашивать целое число до получения допустимого значения."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            print("Введите корректное целое число.")
