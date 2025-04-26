from typing import Generator
from random import randrange

from faker import Faker
import logging

from .base_generator import BaseGenerator


class FakerGenerator(BaseGenerator):
    """
    Класс для получения фейковых пользователей
    """

    def __init__(self):
        """
        Конструктор
        """
        self.__faker = Faker("ru_RU")

    def _get_row(self, num: int) -> tuple[str, ...]:
        """
            Данные о фейковых пользователях

        Args:
            num: номер пользователя с 0

        Returns:
            tuple[str, ...]: список значений в колонках
        """
        if randrange(2):
            get_last_name = self.__faker.last_name_female
            get_first_name = self.__faker.first_name_female
        else:
            get_last_name = self.__faker.last_name_male
            get_first_name = self.__faker.first_name_male

        return (
            get_last_name(),  # 0
            get_first_name(),  # 1
            self.__faker.phone_number(),  # 2
            self.__faker.hostname(),  # 3
            self.__faker.ascii_free_email(),  # 4
            self.__faker.job(),  # 5
            self.__faker.company(),  # 6
            self.__faker.country(),  # 7
            self.__faker.postcode(),  # 8
            self.__faker.address(),  # 9
        )


fake_generator = FakerGenerator()
