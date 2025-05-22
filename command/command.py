from interface import ICommand
from command.exception import Command4Exception
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
        # if self._raise_exception:
        #     raise Command4Exception(f"Exception in {self.__class__.__name__}.execute method")


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
