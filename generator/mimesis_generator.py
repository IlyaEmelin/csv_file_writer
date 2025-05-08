from random import choice

from mimesis import Person, Internet, Finance, Address
from mimesis.enums import Gender
from mimesis.locales import Locale
from .base_generator import BaseGenerator

_ALL_GENDER = list(Gender)

FULL_ADDRESS_INDEX = 9
POSTCODE_INDEX = 8
COUNTRY_INDEX = 7


class MimesisGenerator(BaseGenerator):
    """
    Класс для получения фейковых пользователей
    """

    def __init__(self):
        super().__init__()
        self.__locale = Locale.RU
        self.__person = Person(locale=self.__locale)
        self.__internet = Internet()
        self.__finance = Finance(locale=self.__locale)
        self.__address = Address(locale=self.__locale)

    def _get_row(self, num: int) -> tuple[str, ...]:
        """
        Данные о фейковых пользователях

        Args:
            num: номер строчки с 0

        Returns:
            tuple[str, ...]: список значений в колонках
        """
        gender = choice(_ALL_GENDER)
        return (
            self.__person.last_name(gender=gender),  # 0
            self.__person.first_name(gender=gender),  # 1
            self.__person.phone_number(),  # 2
            self.__internet.hostname(),  # 3
            self.__person.email(),  # 4
            self.__person.occupation(),  # 5
            self.__finance.company(),  # 6
            self.__address.country(),  # 7
            self.__address.postal_code(),  # 8
            self.__address.address(),  # 9
        )
