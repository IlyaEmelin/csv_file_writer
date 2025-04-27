from base_checker import BaseChecker
from time import sleep
from functools import lru_cache
from geopy.geocoders import Nominatim


class Country(BaseChecker):
    """
    Проверяет корректность страны основываясь на данные
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
        Проверяем страну который храниться в одном поле.

        Args:
            *args: аргументы список содержащий страну (1-н аргумент)

        Returns:
            str:
        """
        country = args[0]
        location = self.__geolocator.geocode({"country": country})
        sleep(self.SLEEP_SECONDS)

        if location is None:
            return (
                f"{country} - почтовый индекс является фейковым.\n"
                "Не прошел валидацию на основе данных с сайта openstreetmap."
            )
        return ""
