from base_checker import BaseChecker
from time import sleep
from functools import lru_cache
from geopy.geocoders import Nominatim

from checker.geo_type import GeoType

USER_AGENT_NAME = "user_data_generator"
CACHE_SIZE = 1024 * 16
SLEEP_SECONDS = 1


class GeoChecking(BaseChecker):
    """
    Проверяет корректность переданных гео данных основываясь на данные
    с сайта www.openstreetmap.org
    Использование данной проверки очень сильно замедляет генерацию данных

    ВАЖНО: Запрашивать данные не чаще чем раз в секунду
    Иначе заблокируют

    TODO: В будущем можно еще базу подцепить для сохранения рассчитанных данных
    """

    def __init__(self, geo_type: GeoType) -> None:
        super().__init__()

        self.__geolocator = Nominatim(user_agent=USER_AGENT_NAME)
        self.__geo_type: GeoType = geo_type

    @lru_cache(maxsize=CACHE_SIZE)
    def __cache_check(self, geo_type: GeoType, geo_data: str) -> str:
        """
        Кешируемый метод проверки гео-данных.

        Выделено в отдельный метод так как результат который мы кешируем
        зависит от типа гео данных и их самих

        Args:
            geo_type: тип гео данных
            geo_data: гео данные

        Returns:
            str: текст ошибки в гео-данных
        """
        if geo_data:
            locator_field_name, text_name = geo_type.value
            if locator_field_name:
                location = self.__geolocator.geocode(
                    {
                        locator_field_name: geo_data,
                    }
                )
            else:
                location = self.__geolocator.geocode(geo_data)
            sleep(SLEEP_SECONDS)

            if location is None:
                return (
                    f"{geo_data} - {text_name} является фейковым.\n"
                    "Не прошел валидацию на основе данных с "
                    "сайта openstreetmap."
                )
        return ""

    def check(self, *args) -> str:
        """
        Проверяем гео-данные который храниться в одном поле.

        Args:
            *args: аргументы список содержащий гео-данные (1-н аргумент)

        Returns:
            str: текст ошибки в гео-данных
        """
        geo_data: str = args[0]
        return self.__cache_check(self.__geo_type, geo_data)
