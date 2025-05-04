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
            return ""
        if (len_row := len(args)) != (len_head := len(self.__head)):
            text = (
                f"Длина кортежа полученной из текущей строчки: {args}\n"
                f"не совпадает длиной заголовка: {self.__head}\n"
                f"{len_head} != {len_row}"
            )

            logging.error(
                (
                    f"Длина кортежа полученной из текущей строчки: %s\n"
                    f"не совпадает длиной заголовка: %s\n"
                    f"%s != %s"
                ),
                args,
                self.__head,
                len_head,
                len_row,
            )
            return text
        return ""
