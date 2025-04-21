from abc import abstractmethod
from typing import Generator
import logging


class BaseGenerator:
    """
    Базовый класс для получения данных
    """

    @staticmethod
    def _get_head() -> tuple[
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
        """
            Список название получаемых колонок

        Returns:
            tuple[str, ...]: название колонок которые мы хотим получить
        """
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
    def _get_row(self) -> tuple[str, ...]:
        """
            Список значений в колонках
            длины кортежей из _get_head и _get_row должны совпадать

        Returns:
            tuple[str, ...]: список значений в колонках
        """

    def generate_data(
        self,
        count_line: int,
    ) -> Generator[
        tuple[str, ...],
        None,
        None,
    ]:
        """
        Генератор полученных данных

        Args:
            count_line: количество колонок которые необходимо сгенерировать

        Yields:
            tuple[str, ...]: полученная колонка
        """
        head = self._get_head()
        len_head = len(head)
        yield head
        for i in range(count_line):
            if i * 100 % count_line == 0:
                logging.info(f"write {i * 100 // count_line} %")
            row = self._get_row()
            if (len_row := len(row)) != len_head:
                logging.error(
                    (
                        f"Длина кортежа полученной из текущей строчки: {row}\n",
                        f"не совпадает длиной заголовка: {head}\n",
                        f"{len_head} != {len_row}",
                    )
                )
            yield row
