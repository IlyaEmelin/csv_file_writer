import logging

from .base_checker import BaseChecker


class CountRow(BaseChecker):
    """Класс проверки количества строк к строчке"""

    def __init__(self) -> None:
        self.__head = None

    def check(self, *args) -> str:
        """
        Проверка значений в строчке

        Args:
            *args: значения в колонке
        """
        if self.__head is None:
            self.__head = args
        else:
            if (len_row := len(args)) != (len_head := self.__head):
                text = (
                    f"Длина кортежа полученной из текущей строчки: {args}\n"
                    f"не совпадает длиной заголовка: {self.__head}\n"
                    f"{len_head} != {len_row}"
                )

                logging.error(text)
                return text
        return ""
