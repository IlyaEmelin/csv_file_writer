import csv
from typing import Generator, Final
from datetime import datetime
from zipfile import ZipFile
from os import sep, remove

import logging

from generator.fake_generator import fake_generator
from generator.keyboard_generator import keyboard_generator
from .base_writer_data import BaseWriterData


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

    def __base_compress(
        self,
        data_generator: Generator[tuple[str, ...], None, None],
        csv_file_name: str,
        compresslevel: int = 5,
    ) -> None:
        """
            Базовый метод для сохранения данных в файл архива

        Args:
            data_generator: генератор данных сохраняемый в архив
            csv_file_name: имя scv файла сохраняемого в архив
            compresslevel: уровень сжатия файла
        """
        full_file_name_zip = self.get_full_file_name_zip(csv_file_name)

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
                            self.__delimiter.join(row) + "\r\n",
                            self.__encoding,
                        )
                    )

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

    def get_full_file_name_zip(self, csv_file_name: str) -> str:
        """
        Полный путь к файлу архива в рабочей директории

        Args:
            csv_file_name: имя файла csv

        Returns:
            str: Полный путь к файлу в рабочей директории
        """
        args = self.get_full_file_name_csv(csv_file_name).split(".")
        return ".".join(args[0:-1]) + ".zip"

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
        file_name: str,
        delete_source_file: bool = True,
        compresslevel: int = 5,
    ) -> None:
        """
        Сжать файл csv в архив

        Args:
            file_name: имя csv файла
            delete_source_file: удалить csv файла после сжатия
            compresslevel: степень сжатия [0: 9]
        """
        full_file_name = self.get_full_file_name_csv(file_name)
        full_file_name_zip = self.get_full_file_name_zip(file_name)

        logging.info("Zip file")
        with ZipFile(
            full_file_name_zip,
            "w",
            compresslevel=compresslevel,
        ) as zip_file:
            zip_file.write(
                full_file_name,
                arcname=file_name,
            )

        if delete_source_file:
            logging.info("Delete source file")
            remove(full_file_name)

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
        self.__base_compress(
            data_generator=keyboard_generator.generate_data(self.__count_line),
            csv_file_name=csv_file_name,
            compresslevel=compresslevel,
        )

    def compress_auto_generate(
        self,
        file_name: str | None = None,
        compresslevel: int = 5,
    ) -> None:
        """
        Получение фейковых данных и сжатие результата в архив

        Args:
            file_name: имя csv файла для сжатия
                может быть пустой в этом случае имя файла сформируется на основе текущей даты и времени
            compresslevel: степень сжатия [0: 9]
        """
        file_name = self.__get_csv_file_name(file_name)
        self.__base_compress(
            data_generator=fake_generator.generate_data(self.__count_line),
            csv_file_name=file_name,
            compresslevel=compresslevel,
        )
