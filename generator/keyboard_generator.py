from typing import Generator

from .base_generator import BaseGenerator


class KeyboardGenerator(BaseGenerator):
    def get_user(self) -> tuple[str, ...]:
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

    def generate_data(
        self,
        count_line: int,
    ) -> Generator[
        tuple[str, ...],
        None,
        None,
    ]:
        yield self.get_head()
        for __ in range(count_line):
            yield self.get_user()


keyboard_generator = KeyboardGenerator()
