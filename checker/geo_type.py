from enum import Enum


class GeoType(Enum):
    """Тип проверяемой гео-позиции"""

    FULL_ADDRESS = (None, "полный индекс")
    POSTAL_CODE = ("postal_code", "почтовый индекс")
    COUNTRY = ("country", "страна")
