import csv
from typing import Generator
from datetime import datetime
from zipfile import ZipFile
from os import sep, remove

import logging

from generator.fake_generator import fake_generator
from generator.keyboard_generator import keyboard_generator


class Formater:
    def __init__(
        self,
        count_line: int = 5_000,  # 500_000,
        delimiter: str = ";",
    ):
        self.__path_to_file = "result"
        self.__file_name = None
        self.__count_line = count_line
        self.__delimiter = delimiter

    def __get_file_format(self, file_name: str | None):
        if file_name:
            self.__file_name = file_name
        elif self.__file_name is None:
            self.__file_name = (
                file_name
                if file_name
                else f"{datetime.now().strftime(f"%y-%m-%d  %H-%M-%S")}.csv"
            )
        return self.__file_name

    def __get_csw_writer(self, csvfile):
        csv_writer = csv.writer(
            csvfile,
            delimiter=self.__delimiter,
            quotechar="|",
            quoting=csv.QUOTE_MINIMAL,
        )
        return csv_writer

    def __base_compress(
        self,
        data_generator: Generator[tuple[str, ...], None, None],
        file_name: str | None = None,
        compresslevel: int = 5,
    ) -> None:
        file_name = self.__get_file_format(file_name)
        full_file_name_zip = self.get_full_file_name_zip(file_name)

        logging.info("Create zip file.")
        with ZipFile(
            full_file_name_zip,
            "w",
            compresslevel=compresslevel,
        ) as archive:
            logging.info("Create result file.")
            with archive.open(file_name, "w") as csvfile:
                for row in data_generator:
                    csvfile.write(
                        bytes(
                            ";".join(row) + "\r\n",
                            "utf-8",
                        )
                    )

    @property
    def path_to_file(self) -> str:
        return self.__path_to_file

    def get_full_file_name_csv(self, file_name: str) -> str:
        return sep.join((self.path_to_file, file_name))

    def get_full_file_name_zip(self, file_name: str) -> str:
        args = self.get_full_file_name_csv(file_name).split(".")
        return ".".join(args[0:-1]) + ".zip"

    def write_to_file_csv(self, file_name: str | None = None) -> None:
        file_name = self.__get_file_format(file_name)

        with open(
            self.get_full_file_name_csv(file_name),
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            logging.info("Open file to write result.")

            csv_writer = self.__get_csw_writer(csvfile)
            for row in fake_generator.generate_data(self.__count_line):
                csv_writer.writerow(row)

    def compress_csv_file(
        self,
        file_name: str | None = None,
        delete_source_file: bool = True,
        compresslevel: int = 5,
    ) -> None:
        file_name = self.__get_file_format(file_name)
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
        file_name: str | None = None,
        compresslevel: int = 5,
    ) -> None:
        self.__base_compress(
            data_generator=keyboard_generator.generate_data(self.__count_line),
            file_name=file_name,
            compresslevel=compresslevel,
        )

    def compress_auto_generate(
        self,
        file_name: str | None = None,
        compresslevel: int = 5,
    ) -> None:
        self.__base_compress(
            data_generator=fake_generator.generate_data(self.__count_line),
            file_name=file_name,
            compresslevel=compresslevel,
        )
