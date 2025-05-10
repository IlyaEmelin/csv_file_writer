from typing import Generator, BinaryIO

from core.constants import Constants
from core.helper import get_path
from .base_writer import BaseWriter


class TextWriter(BaseWriter):
    """Класс который, создает txt файл"""

    @property
    def file_type(self) -> str:
        """
        str: расширение файла
        """
        return Constants.FileTypes.FILE_TYPE_TXT

    def write_data(
        self,
        file: BinaryIO,
        data_generator: Generator[tuple[str, ...], None, None],
    ) -> None:
        """
        Запись данных в файл

        Args:
            file: файл куда будет происходить запись
            data_generator: генератор данных
        """
        for row in data_generator:
            file.write(self._get_bytes(row))

    def write(
        self,
        data_generator: Generator[tuple[str, ...], None, None],
    ) -> None:
        """
        Сохранения данных в файл csv напрямую из генератора данных

        Args:
            data_generator: генератор данных сохраняемый в архив
        """
        full_file_name_csv = get_path(
            path_to_file=self._path_to_file,
            file_name=self._file_name,
            file_type=self.file_type,
        )
        with open(full_file_name_csv, "wb") as file_txt:
            self.write_data(file_txt, data_generator)
