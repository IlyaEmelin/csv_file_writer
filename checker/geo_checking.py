from time import sleep
from functools import lru_cache
import logging

from geopy.exc import GeocoderQueryError, GeocoderTimedOut
from geopy.geocoders import Nominatim

from .geo_type import GeoType
from .base_checker import BaseChecker

from core.constants import Constants


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

        self.__geolocator = Nominatim(user_agent=Constants.GeoChecking.USER_AGENT_NAME)
        self.__geo_type: GeoType = geo_type
        self.__is_head_row = True

    @lru_cache(maxsize=Constants.GeoChecking.CACHE_SIZE)
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
        match geo_data, geo_type:
            case geo_data, geo_type if geo_data and geo_type.locator_field_name:
                geo_data = {geo_type.locator_field_name: geo_data}
        if geo_data:
            try:
                location = self.__geolocator.geocode(
                    geo_type.get_geo_data(geo_data),
                    timeout=Constants.GeoChecking.TIMEOUT,
                )
            except (GeocoderQueryError, GeocoderTimedOut):
                logging.error(
                    "Ошибка получения гео данных: %s / %s",
                    geo_data,
                    geo_type.text_name,
                    exc_info=True,
                )
                return (
                    f"Для {geo_data} - типа {geo_type.text_name}\n"
                    "Ошибка получения данных с гео сервиса."
                )
            else:
                sleep(Constants.GeoChecking.SLEEP_SECONDS)

                if location is None:
                    logging.warning(
                        "%s - %s является фейковым.",
                        geo_data,
                        geo_type.text_name,
                    )
                    return (
                        f"{geo_data} - {geo_type.text_name} "
                        "является фейковым.\n"
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
        if self.__is_head_row:
            self.__is_head_row = False
        else:
            geo_data: str = args[0]
            return self.__cache_check(self.__geo_type, geo_data)
