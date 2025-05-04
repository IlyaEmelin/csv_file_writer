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
        # Сделай циклом нормально
        print(f"--- Введите данные о пользователе {num + 1} ---")
        surname = input("Введите фамилию:")
        name = input("Введите имя:")
        phone_number = input("Введите номер телефона:")
        website = input("Введите сайт:")
        email = input("Введите email:")
        profession = input("Введите профессию:")
        company = input("Введите компанию:")
        country = input("Введите название страны:")
        postal_code = input("Введите почтовый индекс:")
        address = input("Введите полный адрес:")
        return (
            surname,
            name,
            phone_number,
            website,
            email,
            profession,
            company,
            country,
            postal_code,
            address,
        )


keyboard_generator = KeyboardGenerator()
