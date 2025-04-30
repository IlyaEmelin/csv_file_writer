from typing import Generator
import logging
import os

from py7zr import SevenZipFile
import tempfile

from .base_writer import BaseWriter
from core.constants import Constants
from core.path_helper import get_path


class Compressor7zWriter(BaseWriter):
    pass

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
        full_file_name_7z = get_path(
            path_to_file=self._path_to_file,
            file_name=self._file_name,
            file_type=Constants.FileTypes.FILE_TYPE_7Z,
        )
        full_file_name_csv = get_path(
            "",
            file_name=self._file_name,
            file_type=Constants.FileTypes.FILE_TYPE_CSV,
        )

        logging.info("Create temporary file.")
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            for row in data_generator:
                tmp.write(self._get_bytes(row))
            tmp_name = tmp.name

        logging.info("Add temporary file to archive")
        with SevenZipFile(full_file_name_7z, "w") as archive:
            archive.write(
                tmp_name,
                arcname=full_file_name_csv,
            )

        logging.info("Delete temporary file")
        os.unlink(tmp_name)
