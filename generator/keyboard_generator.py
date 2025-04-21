from typing import Generator

from .base_generator import BaseGenerator


class KeyboardGenerator(BaseGenerator):
    """
    Класс для получения пользователей введенных с клавиатуры
    """

    def _get_row(self) -> tuple[str, ...]:
        """
            Данные о пользователях введенных с клавиатуры

        Returns:
            tuple[str, ...]: список значений в колонках
        """
        print("-" * 100)
        print("Введите фамилию:")
        surname = input()
        print("Введите имя:")
        name = input()
        print("Введите номер телефона:")
        phone_number = input()
        print("Введите сайт:")
        website = input()
        print("Введите email:")
        email = input()
        print("Введите профессию:")
        profession = input()
        print("Введите компанию:")
        company = input()
        print("Введите название страны:")
        country = input()
        print("Введите почтовый индекс:")
        postal_code = input()
        print("Введите полный адрес:")
        address = input()
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
