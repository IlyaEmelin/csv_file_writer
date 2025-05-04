from enum import Enum

# Может датакласс?
class GeoType(Enum):
    """Тип проверяемой гео-позиции"""

    FULL_ADDRESS = (None, "полный адрес")
    POSTAL_CODE = ("postalcode", "почтовый индекс")
    COUNTRY = ("country", "страна")
