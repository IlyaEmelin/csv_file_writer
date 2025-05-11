from typing import Generator
from zipfile import ZipFile
import multivolumefile
import logging

from writer.base_writer import BaseWriter
from compression.base_comressor import BaseCompressor
from compression.temporary_file import TemporaryFile
from core.constants import Constants
from core.helper import get_path


class CompressorZipCompressor(BaseCompressor):
    """
    Класс для сжатия файлов на основе ZipFile класса
    """

    def write(
        self,
        writer_data: BaseWriter,
        data_generator: Generator[tuple[str, ...], None, None],
        compresslevel: int = 5,
    ) -> None:
        """
        Сохранения данных в файл архива напрямую из генератора данных

        Args:
            writer_data: класс который, записывает данные
            data_generator: генератор данных сохраняемый в архив
            compresslevel: уровень сжатия файла
        """
        # не драй
        full_file_name_zip = get_path(
            path_to_file=self._path_to_file,
            file_name=self._file_name,
            file_type=Constants.FileTypes.FILE_TYPE_ZIP,
        )
        full_file_name_csv = get_path(
            "",
            file_name=self._file_name,
            file_type=writer_data.file_type,
        )

        with TemporaryFile() as temp_file:
            writer_data.write_data(
                file=temp_file,
                data_generator=data_generator,
            )
            temp_file.flush()

            logging.info(
                "Create result file: %s",
                full_file_name_zip,
            )
            with ZipFile(
                full_file_name_zip,
                "w",
                compresslevel=compresslevel,
            ) as archive:
                logging.info("add result file to zip.")
                archive.write(
                    filename=temp_file.name,
                    arcname=full_file_name_csv,
                )
