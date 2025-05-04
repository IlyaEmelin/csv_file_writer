from typing import Generator

from .base_generator import BaseGenerator


class KeyboardGenerator(BaseGenerator):
    """
    Класс для получения пользователей введенных с клавиатуры
    """

    def _get_row(self, num: int) -> tuple[str, ...]:
        """
        Данные о пользователях введенных с клавиатуры

        Args:
            num: номер пользователя с 0

        Returns:
            tuple[str, ...]: список значений в колонках
        """
        print(f"--- Введите данные о пользователе {num + 1} ---")

        return tuple(
            input(f"Введите {name}:")
            for name in (
                "фамилию",
                "имя",
                "номер телефона",
                "сайт",
                "email",
                "профессию",
                "компанию",
                "название страны",
                "почтовый индекс",
                "полный адрес",
            )
        )


keyboard_generator = KeyboardGenerator()
