from typing import Generator
from abc import ABC, abstractmethod
import os


class BaseCompressor(ABC):
    """
    Базовый класс для сжатия файлов
    """

    @staticmethod
    def _get_full_file_name_zip(full_file_name_csv: str) -> str:
        """
        Полный путь к файлу архива в рабочей директории

        Args:
            full_file_name_csv: имя файла csv

        Returns:
            str: Полный путь к файлу в рабочей директории
        """
        args = full_file_name_csv.split(".")
        return ".".join(args[0:-1]) + ".zip"

    @staticmethod
    def _get_file_name(full_file_name_csv: str) -> str:
        # Докстринги лучше писать в одном стиле( с большой буквы первой как выше например)
        # В целом тут можно обойтись без него - говорящее имя функции говорит обо всем
        """
        получить имя файла на основе полного пути к нему

        Args:
            full_file_name_csv: полный путь к файлу и его название

        Returns:

        """
        return full_file_name_csv.split(os.sep)[-1]
    # Эти два методы выглядят как два разных доп класса для масшабирования
    @abstractmethod
    def compress_by_generator(
        self,
        data_generator: Generator[tuple[str, ...], None, None],
        full_csv_file_name: str,
        # Магическое число - вынеси в сетиннги
        compresslevel: int = 5,
    ) -> None:
        """
            Сохранения данных в файл архива напрямую из генератора данных

        Args:
            data_generator: генератор данных сохраняемый в архив
            full_csv_file_name: полный путь к scv файлу сохраняемого в архив
            compresslevel: уровень сжатия файла
        """

    @abstractmethod
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
    # Лучше заставлять разрабов переопределять через NotEmplementError