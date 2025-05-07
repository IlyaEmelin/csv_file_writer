from datetime import datetime
from typing import Generator
from abc import ABC, abstractmethod

from core.constants import Constants
from writer.base_writer import BaseWriter


class BaseCompressor(ABC):
    """Базовый класс для сжатия объектов"""

    def __init__(
        self,
        file_name: str | None = None,
        path_to_file: str | None = Constants.File.DEFAULT_PATH_TO_FILE,
    ):
        """
        Класс для сжатия файлов на основе ZipFile класса

        Args:
            file_name: имя файла
            path_to_file: путь к файлу
        """
        self._file_name = (
            file_name
            if file_name
            else datetime.now().strftime(Constants.File.BASE_FILE_RESULT_FORMAT)
        )
        self._path_to_file = path_to_file

    @abstractmethod
    def write(
        self,
        writer_data: BaseWriter,
        data_generator: Generator[tuple[str, ...], None, None],
        compression_level: int = 5,
    ) -> None:
        """
        Сохранения данных в файл архива напрямую из генератора данных

        Args:
            writer_data: класс который, записывает данные
            data_generator: генератор данных сохраняемый в архив
            compression_level: уровень сжатия файла
        """
