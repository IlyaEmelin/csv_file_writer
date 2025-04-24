import os
from typing import Generator, Final
from zipfile import ZipFile
import logging

from .base_compressor import BaseCompressor


class ZipFileCompressor(BaseCompressor):
    """
    Класс для сжатия файлов на основе ZipFile класса
    """

    END_ROW = "\r\n"

    # Типизация!
    def __init__(self, delimiter, encoding):
        # В конструкторе докстринг лишний чаще всего
        """
        Конструктор

        Args:
            delimiter: разделитель колонок
            encoding: кодировка файла
        """
        self.__delimiter = delimiter
        self.__encoding = encoding

    def compress_by_generator(
        self,
        data_generator: Generator[tuple[str, ...], None, None],
        full_csv_file_name: str,
        compresslevel: int = 5,
    ) -> None:
        """
            Сохранения данных в файл архива напрямую из генератора данных

        Args:
            data_generator: генератор данных сохраняемый в архив
            full_csv_file_name: полный путь к scv файлу сохраняемого в архив
            compresslevel: уровень сжатия файла
        """
        full_file_name_zip = self._get_full_file_name_zip(full_csv_file_name)
        csv_file_name = self._get_file_name(full_csv_file_name)

        logging.info("Create zip file.")
        with ZipFile(
            full_file_name_zip,
            "w",
            compresslevel=compresslevel,
        ) as archive:
            logging.info("Create result file.")
            with archive.open(csv_file_name, "w") as csvfile:
                for row in data_generator:
                    csvfile.write(
                        bytes(
                            self.__delimiter.join(row) + self.END_ROW,
                            self.__encoding,
                        )
                    )

    def compress_by_csv_file(
        self,
        full_file_name_csv: str,
        compresslevel: int = 5,
    ) -> None:
        """
            Сохранения данных в файл архива из csv файла

        Args:
            full_file_name_csv: полный путь к csv файлу
            compresslevel: уровень сжатия файла
        """
        full_file_name_zip = self._get_full_file_name_zip(full_file_name_csv)

        logging.info("Zip file")
        with ZipFile(
            full_file_name_zip,
            "w",
            compresslevel=compresslevel,
        ) as zip_file:
            zip_file.write(
                full_file_name_csv,
                arcname=self._get_file_name(full_file_name_csv),
            )
