from typing import Generator, Any
import logging

from py7zr import SevenZipFile, FILTER_LZMA2
import multivolumefile

from compression.base_comressor import BaseCompressor
from compression.temporary_file import TemporaryFile
from writer.base_writer import BaseWriter
from core.constants import Constants
from core.helper import get_path


class Compressor7zCompressor(BaseCompressor):
    """
    Класс для записи данных в архив 7z
    """

    @staticmethod
    def __write_to_archive(
        full_file_name_7z: str,
        full_file_name_csv: str,
        filters: dict[str:Any],
        tmp_name: str,
        volume: int | None,
    ) -> None:
        """
        Запись файла в архив

        Args:
            full_file_name_7z: полное имя файла 7z
            full_file_name_csv: полное имя файла csv
            filters: фильтр для архивации
            tmp_name: имя временного файла
            volume: размер тома
        """
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

    def write(
        self,
        writer_data: BaseWriter,
        data_generator: Generator[tuple[str, ...], None, None],
        compression_level: int = 5,
        volume: int | None = None,
    ) -> None:
        """
        Сохранения данных в файл архива напрямую из генератора данных

        Args:
            writer_data: класс который, записывает данные
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
            file_type=writer_data.file_type,
        )

        with TemporaryFile() as temp_file:
            writer_data.write_data(
                file=temp_file,
                data_generator=data_generator,
            )
            temp_file.flush()

            logging.info("Add temporary file to archive 7z")
            filters = [
                {
                    "id": FILTER_LZMA2,
                    # Уровень сжатия от 0 до 9
                    "preset": compression_level,
                    # Размер словаря (можно настроить)
                    "dict_size": 16 * 1024 * 1024,
                }
            ]
            self.__write_to_archive(
                full_file_name_7z,
                full_file_name_csv,
                filters,
                temp_file.name,
                volume,
            )
