from base_checker import BaseChecker
from time import sleep
from functools import lru_cache
from geopy.geocoders import Nominatim


class PostalCode(BaseChecker):
    """
    Проверяет корректность почтового индекса основываясь на данные
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
        Проверяем почтовый индекс который храниться в одном поле.

        Args:
            *args: аргументы список содержащий почтовый индекс (1-н аргумент)

        Returns:
            str:
        """
        postal_code = args[0]
        location = self.__geolocator.geocode({"postal_code": postal_code})
        sleep(self.SLEEP_SECONDS)

        if location is None:
            return (
                f"{postal_code} - почтовый индекс является фейковым.\n"
                "Не прошел валидацию на основе данных с сайта openstreetmap."
            )
        return ""
