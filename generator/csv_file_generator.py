from typing import Generator
from itertools import chain

from .base_generator import BaseGenerator
from core.constants import Constants
from core.path_helper import get_path

CSV_FILE_TYPE = "csv"


class CsvFileGenerator(BaseGenerator):
    """
    Генератор данных на основе CSV файла
    """

    def __init__(
        self,
        file_name: str,
        path_to_file: str = Constants.DEFAULT_PATH_TO_FILE,
        encoding: str = Constants.DEFAULT_ENCODING,
        delimiter: str = Constants.ROW_DELIMITER,
    ) -> None:
        """
        Генератор данных на основе CSV файла

        Args:
            file_name: имя файла
            path_to_file: путь к файлу
            encoding: кодировка файла
            delimiter: разделитель строк
        """
        super().__init__()
        self.__file_name = file_name
        self.__path_to_file = path_to_file
        self.__encoding = encoding
        self.__delimiter = delimiter

    def _get_row(self, num: int) -> tuple[str, ...]:
        """
        Данные в колонках вычитанные из файла

        Args:
            num: номер строчки с 0

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
        with open(
            get_path(
                path_to_file=self.__path_to_file,
                file_name=self.__file_name,
                file_type=CSV_FILE_TYPE,
            ),
            "r",
            encoding=self.__encoding,
        ) as csvfile:
            # певая строка не с данными, а названиями колонок
            file_line = csvfile.readline()
            if file_line:
                while True:
                    file_line = csvfile.readline()
                    if not file_line:
                        break
                    row = tuple(file_line.split(self.__delimiter))
                    text_problem = self._check_row(row)
                    if self.add_row_problem:
                        row = tuple(chain(row, (text_problem,)))
                    yield row
