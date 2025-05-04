from itertools import chain
from abc import abstractmethod
from typing import Generator
import logging

from checker.base_checker import BaseChecker
from core.constants import Constants


class BaseGenerator:
    """Базовый класс для получения данных"""

    def __init__(self):
        """Конструктор базовый класс для получения данных"""
        self.__checkers: list[tuple[tuple[int, ...] | None, BaseChecker]] = []
        # Добавлять в результат колонку с проблемами
        self.add_row_problem: bool = False

    def __get_row(
        self,
        index_cols_to_check: tuple[int, ...] | None,
        row: tuple[str, ...],
    ) -> tuple[str, ...]:
        """
        Получить значения строк которые будем проверять

        Args:
            index_cols_to_check: индексы проверяемых строк
            row: значения строк

        Returns:
            tuple[str, ...]: значения проверяемых строк
        """
        if index_cols_to_check is None:
            return row
        else:
            try:
                return tuple(row[index_col] for index_col in index_cols_to_check)
            except IndexError:
                logging.error(
                    "В классе %s, индекс запрашиваемой колонки выходит "
                    "за диапазон колонок.\n"
                    "Проверьте первый парaметр переданный "
                    "в метод add_checker.\n",
                    self,
                    exc_info=True,
                )
        return tuple()

    def _check_row(self, row: tuple[str, ...]) -> str:
        """
        Проверка переданной строчки значений

        Args:
            row: строчка значений

        Returns:
            str: результат проверки
        """
        result = []
        for index_cols_to_check, checker in self.__checkers:
            check_row = self.__get_row(index_cols_to_check, row)
            if check_row:
                text = checker.check(*row)
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
            "Фамилия",  # 0
            "Имя",  # 1
            "Номер телефона",  # 2
            "Сайт",  # 3
            "email",  # 4
            "Профессия",  # 5
            "Компания",  # 6
            "Название страны",  # 7
            "Почтовый индекс",  # 8
            "Полный адрес",  # 9
        )
        if self.add_row_problem:
            return tuple(chain(head, ("Ошибки валидации",)))
        return head

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
        count_line: int = Constants.DEFAULT_COUNT_ROW,
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
        self._check_row(head)

        yield head
        for i in range(count_line):
            if i * 100 % count_line == 0:
                logging.info(
                    "write %s %",
                    i * 100 // count_line,
                )
            row = self._get_row(i)
            text_problem = self._check_row(row)
            if self.add_row_problem:
                row = tuple(chain(row, (text_problem,)))
            yield row
