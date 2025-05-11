from enum import Enum
from typing import Union

class GeoType(Enum):
    """Тип проверяемой гео-позиции"""

    FULL_ADDRESS = (None, "полный адрес")
    POSTAL_CODE = ("postalcode", "почтовый индекс")
    COUNTRY = ("country", "страна")

    def get_geo_data(self, geo_data: str) -> Union[str | dict[str, str]]:
        """
        Получить объект гео данных для вызова на сервис

        Args:
            geo_data: гео-данные которые хотим получить

        Returns:
            Union[str | dict[str, str]]: объект для запроса geocode
        """
        # Лучше добавить доп проперти для возврата нужного значения - будет читаемо
        if locator_field_name := self.value[0]:
            return {locator_field_name: geo_data}
        return geo_data

    @property
    def text_name(self):
        return self.value[1]
