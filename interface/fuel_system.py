from abc import ABC, abstractmethod


class IFuelSystem(ABC):

    @abstractmethod
    def get_fuel_level(self) -> int:
        """Возвращает текущий уровень топлива."""
        pass

    @abstractmethod
    def consume(self, amount: int):
        """Уменьшает количество топлива на заданное число."""
        pass
