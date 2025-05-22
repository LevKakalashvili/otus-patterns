from command import CommandException
from interface import IFuelSystem


class StarShipFuelSystem(IFuelSystem):
    def __init__(self, initial_fuel: int):
        self._fuel = initial_fuel

    def get_fuel_level(self) -> int:
        return self._fuel

    def consume(self, amount: int):
        if amount > self._fuel:
            raise CommandException("У нашего корабля закончилось топливо")
        self._fuel -= amount
