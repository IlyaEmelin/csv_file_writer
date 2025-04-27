from abc import ABC, abstractmethod


class BaseChecker(ABC):
    """Базовый класс для проверки"""

    @abstractmethod
    def check(self, *args) -> str:
        """
        Проверка значений в строчке

        Args:
            *args: значения в колонке
        """
