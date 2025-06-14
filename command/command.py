from interface import ICommand, IFuelSystem
from command.exception import CommandException
from collections import deque


class Command1(ICommand):

    def execute(self):
        print(f"{self.__class__.__name__}: execute")


class Command2(ICommand):

    def execute(self):
        print(f"{self.__class__.__name__}: execute")


class Command3(ICommand):

    def execute(self):
        print(f"{self.__class__.__name__}: execute")


class Command4(ICommand):
    def __init__(self, raise_exception: bool = False):
        self._raise_exception = raise_exception

    def execute(self):
        print(f"{self.__class__.__name__}: execute")


class CommandWriteToLog(ICommand):
    """Команда, которая записывает информацию о выброшенном исключении в лог"""

    def __init__(self, logger, exception: Exception):
        self._logger = logger
        self._exception = exception

    def execute(self):
        print(f"{self.__class__.__name__}: execute")
        self._logger.exception(self._exception)


class CommandRepeatOnce(ICommand):
    """Команда, которая повторяет Команду, выбросившую исключение"""

    def __init__(self, command: ICommand, event_loop: object):
        self._command = command
        self._event_loop = event_loop

    def execute(self):
        """Ставим команду, бросившую эксепшен в очередь"""
        print(
            f"{self.__class__.__name__}: ставим {self._command.__class__.__name__} в очередь"
        )
        self._event_loop.add_command(self._command)


class CommandRepeatTwice(ICommand):
    """Команда, которая повторяет Команду, выбросившую исключение.
    Количество повторов 2, а потом пишет в лог"""

    def __init__(self, command: ICommand, queue: deque):
        self._command = command
        self._queue = queue

    def execute(self):
        """Ставим команду, бросившую эксепшен в очередь"""
        print(
            f"{self.__class__.__name__}: ставим {self._command.__class__.__name__} в очередь"
        )
        self._queue.append(self._command)


class CommandMove(ICommand):
    def __init__(self, obj: object):
        self._obj = obj

    def execute(self):
        self._obj.move()


class CommandRotate(ICommand):
    def __init__(self, obj: object):
        self._obj = obj

    def execute(self):
        self._obj.rotate()


class CommandCheckFuel(ICommand):
    """Команда, которая проверяет, что топлива достаточно, если нет, то выбрасывает
    исключение CommandException"""

    def __init__(self, fuel_system: IFuelSystem, required_fuel: int):
        self._fuel_system = fuel_system
        self._required_fuel = required_fuel

    def execute(self):
        """Проверяем топливо"""
        if self._fuel_system.get_fuel_level() < self._required_fuel:
            raise CommandException("Недостаточно топлива")


class CommandBurnFuel(ICommand):
    """Команда, которая уменьшает количество топлива на скорость расхода топлива"""

    def __init__(self, fuel_system: IFuelSystem, burn_amount: int):
        self._fuel_system = fuel_system
        self._burn_amount = burn_amount

    def execute(self):
        """Сжигаем топливо"""
        self._fuel_system.consume(self._burn_amount)


class MacroCommand(ICommand):
    """Команда, которая выполняет список команд"""

    def __init__(self, commands: list[ICommand]):
        self._commands = commands

    def execute(self):
        for cmd in self._commands:
            cmd.execute()


class CommandMoveWithFuel(ICommand):
    """Команда движения по прямой с расходом топлива"""

    def __init__(self, fuel_system: IFuelSystem, required_fuel: int, obj_to_move):
        self._macro = MacroCommand(
            [
                CommandCheckFuel(fuel_system=fuel_system, required_fuel=required_fuel),
                CommandMove(obj=obj_to_move),
                CommandBurnFuel(fuel_system=fuel_system, burn_amount=required_fuel),
            ]
        )

    def execute(self):
        self._macro.execute()


class CommandChangeVelocity(ICommand):
    """Команда модифицирует вектор мгновенной скорости, если объект находится в движении"""

    def __init__(self, obj: object):
        self._obj = obj

    def execute(self):
        if hasattr(self._obj, "is_moving") and self._obj.is_moving():
            self._obj.adjust_velocity()


class CommandRotateWithVelocityChange(ICommand):
    """Команда поворота с корректировкой вектора скорости (если объект движется)"""

    def __init__(self, obj):
        self._macro = MacroCommand(
            [
                CommandRotate(obj),
                CommandChangeVelocity(obj),
            ]
        )

    def execute(self):
        self._macro.execute()


class DummyCommand:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        print(f"[DummyCommand] Executing with args={self.args}, kwargs={self.kwargs}")
