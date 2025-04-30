from typing import Generator
from abc import ABC, abstractmethod

from core.constants import Constants
from datetime import datetime


class BaseWriter(ABC):
    """
    Базовый класс для сжатия файлов
    """

    def __init__(
        self,
        file_name: str | None = None,
        path_to_file: str | None = Constants.File.DEFAULT_PATH_TO_FILE,
        delimiter: str = Constants.File.ROW_DELIMITER,
        encoding: str = Constants.File.DEFAULT_ENCODING,
    ):
        """
        Класс для сжатия файлов на основе ZipFile класса

        Args:
            file_name: имя файла
            path_to_file: путь к файлу
            delimiter: разделитель колонок
            encoding: кодировка файла
        """
        self._file_name = (
            file_name
            if file_name
            else datetime.now().strftime(Constants.File.BASE_FILE_RESULT_FORMAT)
        )
        self._path_to_file = path_to_file
        self._delimiter = delimiter
        self._encoding = encoding

    @property
    def file_name(self) -> str:
        """
        str: имя файла без расширения
        """
        return self._file_name

    def _get_bytes(self, row: tuple[str, ...]) -> bytes:
        """
        Возвращает байты который будут записаны в файл

        Args:
            row: tuple значений колонок записываемые в файл

        Returns:
            bytes: байты записываемые в файл
        """
        return bytes(
            self._delimiter.join(row) + Constants.File.END_ROW,
            self._encoding,
        )

    @abstractmethod
    def write(
        self,
        data_generator: Generator[tuple[str, ...], None, None],
    ) -> None:
        """
            Сохранения данных в файл архива напрямую из генератора данных

        Args:
            data_generator: генератор данных сохраняемый в архив
        """
