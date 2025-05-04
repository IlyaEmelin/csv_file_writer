import csv
from typing import Generator, Final
from datetime import datetime
from zipfile import ZipFile
from os import sep, remove

import logging

from compressor.base_compressor import BaseCompressor
from generator.fake_generator import fake_generator
from generator.keyboard_generator import keyboard_generator
from compressor.zip_file_compressor import ZipFileCompressor
from .base_writer_data import BaseWriterData
#Это не ООП - это просто класс
# Отсуствует единый интерфейс взаимодействия - в названиях функций присуствует указание на конретику - нет универсальности
# Некорретное название
class WriterData(BaseWriterData):
    """
    Класс для записи данных в файл
    """

    DEFAULT_PATH_TO_FILE: Final[str] = "result"
    DEFAULT_ENCODING: Final[str] = "utf-8"
    BASE_FILE_RESULT_FORMAT = "%y-%m-%d  %H-%M-%S"

    def __init__(
        self,
        count_line: int = 500_000,
        delimiter: str = ";",
    ):
        """
        Класс для записи данных в файл

        Args:
            count_line: количество файлов в результате
            delimiter: разделитель для колонок в csv файлах
        """
        self.__path_work_dir = self.DEFAULT_PATH_TO_FILE
        self.__encoding = self.DEFAULT_ENCODING

        self.__count_line = count_line
        self.__delimiter = delimiter

        self.__compressor: BaseCompressor = ZipFileCompressor(
            delimiter=self.__delimiter,
            encoding=self.__encoding,
        )

    def __get_csv_file_name(self, file_name: str | None) -> str:
        """
        Метод для возвращения имени файла
        если задано пустое название файла
        то название файла будет формироваться на основе текущей даты и времени

        Args:
            file_name: имя файла

        Returns:
            str: имя csv файла
        """
        if file_name:
            return file_name
        return f"{datetime.now().strftime(self.BASE_FILE_RESULT_FORMAT)}.csv"

    @property
    def path_work_dir(self) -> str:
        """
        str: путь к рабочей директории
        """
        return self.__path_work_dir

    def get_full_file_name_csv(self, csv_file_name: str) -> str:
        """
        Полный путь к файлу csv в рабочей директории

        Args:
            csv_file_name: имя файла csv

        Returns:
            str: Полный путь к файлу в рабочей директории
        """
        return sep.join((self.path_work_dir, csv_file_name))

    def write_fake_data_to_file_csv(self, file_name: str | None = None) -> str:
        """
            Запись фейковых данных в файл csv
        Args:
            file_name: имя файла,
                может быть пустой в этом случае имя файла сформируется на основе текущей даты и времени

        Returns:
             str: имя созданного файла
        """
        file_name = self.__get_csv_file_name(file_name)

        with open(
            self.get_full_file_name_csv(file_name),
            "w",
            newline="",
            encoding=self.__encoding,
        ) as csvfile:
            logging.info("Open file to write result.")

            csv_writer = csv.writer(
                csvfile,
                delimiter=self.__delimiter,
                quotechar="|",
                quoting=csv.QUOTE_MINIMAL,
            )
            for row in fake_generator.generate_data(self.__count_line):
                csv_writer.writerow(row)
        return file_name

    def compress_csv_file(
        self,
        csv_file_name: str,
        delete_source_file: bool = True,
        compresslevel: int = 5,
    ) -> None:
        """
        Сжать файл csv в архив

        Args:
            csv_file_name: имя csv файла
            delete_source_file: удалить csv файла после сжатия
            compresslevel: степень сжатия [0: 9]
        """
        full_file_name_csv = self.get_full_file_name_csv(csv_file_name)

        self.__compressor.compress_by_csv_file(
            full_file_name_csv=full_file_name_csv,
            compresslevel=compresslevel,
        )

        if delete_source_file:
            logging.info("Delete source file")
            remove(full_file_name_csv)

    def compress_keyboard(
        self,
        csv_file_name: str | None = None,
        compresslevel: int = 5,
    ) -> None:
        """
        Получение данных с клавиатуры и сжатие результата в архив

        Args:
            csv_file_name: имя csv файла для сжатия
                может быть пустой в этом случае имя файла сформируется на основе текущей даты и времени
            compresslevel: степень сжатия [0: 9]
        """
        csv_file_name = self.__get_csv_file_name(csv_file_name)
        full_csv_file_name = self.get_full_file_name_csv(csv_file_name)
        self.__compressor.compress_by_generator(
            data_generator=keyboard_generator.generate_data(
                self.__count_line,
            ),
            full_csv_file_name=full_csv_file_name,
            compresslevel=compresslevel,
        )

    def compress_auto_generate(
        self,
        csv_file_name: str | None = None,
        compresslevel: int = 5,
    ) -> None:
        """
        Получение фейковых данных и сжатие результата в архив

        Args:
            csv_file_name: имя csv файла для сжатия
                может быть пустой в этом случае имя файла сформируется на основе текущей даты и времени
            compresslevel: степень сжатия [0: 9]
        """
        csv_file_name = self.__get_csv_file_name(csv_file_name)
        full_csv_file_name = self.get_full_file_name_csv(csv_file_name)
        self.__compressor.compress_by_generator(
            data_generator=fake_generator.generate_data(self.__count_line),
            full_csv_file_name=full_csv_file_name,
            compresslevel=compresslevel,
        )
