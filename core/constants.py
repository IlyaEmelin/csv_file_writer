from typing import Final


class Constants:
    """Константы"""

    DEFAULT_COUNT_ROW = 500_000

    class File:
        DEFAULT_PATH_TO_FILE: Final[str] = "result"
        BASE_FILE_RESULT_FORMAT = "%y-%m-%d  %H-%M-%S"
        DEFAULT_ENCODING: Final[str] = "utf-8"
        END_ROW: Final[str] = "\r\n"
        ROW_DELIMITER: Final[str] = ";"

    class FileTypes:
        """Доступные типы файлов"""

        ZIP_FILE_TYPE: Final[str] = "zip"
        CSV_FILE_TYPE: Final[str] = "csv"

    class GeoChecking:
        """Параметры гео-локации"""

        USER_AGENT_NAME: Final[str] = "user_data_generator"
        CACHE_SIZE: Final[int] = 1024 * 16
        SLEEP_SECONDS: Final[int] = 1
        TIMEOUT: Final[int] = 10
