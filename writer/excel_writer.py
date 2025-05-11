import logging
from typing import Generator, BinaryIO
from openpyxl import Workbook


from core.constants import Constants
from core.helper import get_path
from writer.base_writer import BaseWriter


class ExcelWriter(BaseWriter):
    """Класс который, создает excel файл"""

    @property
    def file_type(self) -> str:
        """
        str: расширение файла
        """
        return Constants.FileTypes.FILE_TYPE_EXCEL

    @staticmethod
    def __fill_work_book(
        data_generator: Generator[tuple[str, ...], None, None],
    ) -> Workbook:
        """
        Заполнить книгу для сохранения в файл

        Args:
            data_generator: генератор данных для книги

        Returns:
            Workbook: книга excel с данными
        """
        work_book = Workbook()
        work_sheet = work_book.active
        work_sheet.title = "данные"
        for row, args in enumerate(data_generator):
            for column, value in enumerate(args):
                work_sheet.cell(
                    row=row + 1,
                    column=column + 1,
                    value=value,
                )
        return work_book

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
        work_book = self.__fill_work_book(data_generator)
        logging.info("Save work book")
        work_book.save(file.name)

    def write(
        self,
        data_generator: Generator[tuple[str, ...], None, None],
    ) -> None:
        """
        Сохранения данных в файл excel напрямую из генератора данных

        Args:
            data_generator: генератор данных сохраняемый в архив
        """
        full_file_name_xlsx = get_path(
            path_to_file=self._path_to_file,
            file_name=self._file_name,
            file_type=self.file_type,
        )

        logging.info("Fill work book")
        work_book = self.__fill_work_book(data_generator)
        logging.info("Save work book")
        work_book.save(full_file_name_xlsx)
