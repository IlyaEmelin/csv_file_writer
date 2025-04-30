import os
from typing import Generator, Final
from zipfile import ZipFile
import logging

from .base_writer import BaseWriter
from core.constants import Constants
from core.path_helper import get_path


class ZipCompressorWriter(BaseWriter):
    """
    Класс для сжатия файлов на основе ZipFile класса
    """

    def write(
        self,
        data_generator: Generator[tuple[str, ...], None, None],
        compresslevel: int = 5,
    ) -> None:
        """
        Сохранения данных в файл архива напрямую из генератора данных

        Args:
            data_generator: генератор данных сохраняемый в архив
            compresslevel: уровень сжатия файла
        """
        full_file_name_zip = get_path(
            path_to_file=self._path_to_file,
            file_name=self._file_name,
            file_type=Constants.FileTypes.ZIP_FILE_TYPE,
        )
        full_file_name_csv = get_path(
            "", file_name=self._file_name, file_type=Constants.FileTypes.CSV_FILE_TYPE
        )

        logging.info("Create zip file.")
        with ZipFile(
            full_file_name_zip,
            "w",
            compresslevel=compresslevel,
        ) as archive:
            logging.info("Create result file.")
            with archive.open(full_file_name_csv, "w") as csvfile:
                for row in data_generator:
                    csvfile.write(self._get_bytes(row))
