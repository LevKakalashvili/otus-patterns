import loguru

from command import CommandWriteToLog, CommandRepeatOnce
from interface import ICommand
from collections import deque


class BaseHandler(ICommand):

    def __init__(self, command: ICommand, exception: Exception, queue: deque):
        self._command = command
        self._exception = exception
        self._queue = queue

    def execute(self):
        print(f"{self.__class__.__name__}: handle")


class DefaultHandler(BaseHandler): ...


class Handler1(BaseHandler): ...


class Handler2(BaseHandler): ...


class Handler3(BaseHandler): ...


class Handler4(BaseHandler):
    def execute(self):
        # добавляем в очередь команду
        self._queue.append(
            CommandWriteToLog(logger=loguru.logger, exception=self._exception)
        )


class HandlerRepeaterCommand(BaseHandler):
    def execute(self):
        # добавляем в очередь команду
        self._queue.append(CommandRepeatOnce(command=self._command, queue=self._queue))
