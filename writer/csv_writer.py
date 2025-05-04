from typing import Generator

from core.constants import Constants
from core.helper import get_path
from writer.base_writer import BaseWriter

class CsvWriter(BaseWriter):

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
            file_type=Constants.FileTypes.FILE_TYPE_CSV,
        )
        with open(full_file_name_csv, "wb") as csvfile:
            for row in data_generator:
                csvfile.write(self._get_bytes(row))
