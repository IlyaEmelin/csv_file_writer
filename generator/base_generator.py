from itertools import chain
from abc import abstractmethod
from typing import Generator
import logging

from checker.base_checker import BaseChecker


class BaseGenerator:
    """Базовый класс для получения данных"""

    def __init__(self):
        """Базовый класс для получения данных"""
        self.__checkers: list[tuple[tuple[int, ...] | None, BaseChecker]] = []
        # Добавлять в результат колонку с проблемами
        self.add_row_problem = False

    def __check_row(self, row: tuple[str, ...]) -> str:
        """
        Проверка переданной строчки значений

        Args:
            row: строчка значений

        Returns:
            str: результат проверки
        """
        result = []
        for index_cols_to_check, checker in self.__checkers:
            if index_cols_to_check is None:
                text = checker.check(*row)
                if text:
                    result.append(text)
            else:
                try:
                    args = tuple(row[index_col] for index_col in index_cols_to_check)
                except IndexError as exp:
                    logging.error(
                        (
                            f"В классе {self}, "
                            "индекс запрашиваемой колонки выходит "
                            "за диапазон колонок.\n"
                            "Проверьте первый парaметр переданный "
                            "в метод add_checker.\n"
                        )
                        + str(exp)
                    )
                else:
                    text = checker.check(args)
                    if text:
                        result.append(text)
        return "\n".join(result)

    def add_checker(
        self,
        index_cols_to_check: tuple[int, ...] | None,
        checker: BaseChecker,
    ) -> None:
        """
        Добавить класс,
        который будет проверять значения строчек на корректность

        Args:
            index_cols_to_check: индексы строк, которые отправятся на проверку.
                None - Все строки
            checker: класс, который будет осуществлять проверку
        """
        self.__checkers.append((index_cols_to_check, checker))

    def clear_checkers(self) -> None:
        """Удаляет все классы проверки"""
        self.__checkers.clear()

    def _get_head(self) -> tuple[str, ...]:
        """
            Список название получаемых колонок

        Returns:
            tuple[str, ...]: название колонок которые мы хотим получить
        """
        head = (
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
        if self.add_row_problem:
            return tuple(chain(head, ("Ошибки валидации",)))

    @abstractmethod
    def _get_row(self, num: int) -> tuple[str, ...]:
        """
            Список значений в колонках
            длины кортежей из _get_head и _get_row должны совпадать
        Args:
            num: номер пользователя с 0

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

        self.__check_row(head)

        yield head
        for i in range(count_line):
            if i * 100 % count_line == 0:
                logging.info(f"write {i * 100 // count_line} %")
            row = self._get_row(i)
            text_problem = self.__check_row(row)
            if self.add_row_problem:
                row = tuple(chain(row, (text_problem,)))
            yield row
