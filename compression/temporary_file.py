from tempfile import NamedTemporaryFile
import os
import logging


class TemporaryFile:
    """класс временного файла"""

    def __enter__(self):
        logging.info("Create temporary file.")
        self.__temp_file = NamedTemporaryFile(delete=False)
        return self.__temp_file

    def __exit__(self, type_value, value, traceback):
        logging.info("Close temporary file.")
        file_name = self.__temp_file.name
        self.__temp_file.close()

        os.unlink(file_name)
