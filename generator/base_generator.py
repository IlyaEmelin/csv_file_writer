from abc import abstractmethod
from typing import Generator


class BaseGenerator:
    @staticmethod
    def get_head() -> tuple[
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
    ]:
        return (
            "Фамилия",
            "Имя",
            "Номер телефона",
            "Сайт",
            "email",
            "Профессия",
            "Компания",
            "Название страны",
            "Почтовый индекс",
            "Полный адрес",
        )

    @abstractmethod
    def get_user(self) -> tuple[str, ...]:
        pass

    @abstractmethod
    def generate_data(
        self,
        count_line: int,
    ) -> Generator[
        tuple[str, ...],
        None,
        None,
    ]:
        pass
