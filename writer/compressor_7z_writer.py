from typing import Generator
import logging
import os

from py7zr import SevenZipFile, FILTER_LZMA2
import multivolumefile
import tempfile

from .base_writer import BaseWriter
from core.constants import Constants
from core.path_helper import get_path


class Compressor7zWriter(BaseWriter):
    """
    Класс для записи данных в архив 7z
    """

    def write(
        self,
        data_generator: Generator[tuple[str, ...], None, None],
        compression_level: int = 5,
        volume: int | None = None,
    ) -> None:
        """
        Сохранения данных в файл архива напрямую из генератора данных

        Args:
            data_generator: генератор данных сохраняемый в архив
            compression_level: уровень сжатия файла
            volume: размер файла архива, None - единым архивом
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
        filters = [
            {
                "id": FILTER_LZMA2,
                # Уровень сжатия от 0 до 9
                "preset": compression_level,
                # Размер словаря (можно настроить)
                "dict_size": 16 * 1024 * 1024,
            }
        ]
        if volume is None:
            with SevenZipFile(
                full_file_name_7z,
                "w",
                filters=filters,
            ) as archive:
                archive.write(
                    tmp_name,
                    arcname=full_file_name_csv,
                )
        else:
            with multivolumefile.open(
                full_file_name_7z,
                mode="wb",
                volume=volume,
            ) as target_archive:
                with SevenZipFile(
                    target_archive,
                    "w",
                    filters=filters,
                ) as archive:
                    archive.write(
                        tmp_name,
                        arcname=full_file_name_csv,
                    )

        logging.info("Delete temporary file")
        os.unlink(tmp_name)
