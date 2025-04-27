from base_checker import BaseChecker
from time import sleep
from functools import lru_cache
from geopy.geocoders import Nominatim


class FullAddress(BaseChecker):
    """
    Проверяет корректность полного адресса основываясь на данные
    с сайта www.openstreetmap.org
    Использование данной проверки очень сильно замедляет генерацию данных

    ВАЖНО: Запрашивать данные не чаще чем раз в секунду
    Заблокируют

    TODO: В будущем можно еще базу подцепить для сохранения рассчитанных данных
    """

    USER_AGENT_NAME = "user_data_generator"
    CACHE_SIZE = 1024 * 16
    SLEEP_SECONDS = 1

    def __init__(self) -> None:
        self.__geolocator = Nominatim(user_agent=self.USER_AGENT_NAME)

    @lru_cache(maxsize=CACHE_SIZE)
    def check(self, *args) -> str:
        """
        Проверяем полный адрес который храниться в одном поле.

        Args:
            *args: аргументы список содержащий полный адрес (1-н аргумент)

        Returns:
            str:
        """
        full_address = args[0]
        location = self.__geolocator.geocode(full_address)
        sleep(self.SLEEP_SECONDS)

        if location is None:
            return (
                f"{full_address} - адрес является фейковым.\n"
                "Не прошел валидацию на основе данных с сайта openstreetmap."
            )
        return ""
