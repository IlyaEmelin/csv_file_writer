from abc import ABC, abstractmethod


class BaseWriterData(ABC):
    @abstractmethod
    def write_fake_data_to_file_csv(self, file_name: str | None = None) -> str:
        """
            Запись фейковых данных в файл csv
        Args:
            file_name: имя файла,
                может быть пустой в этом случае имя файла сформируется на основе текущей даты и времени

        Returns:
             str: имя созданного файла
        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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
