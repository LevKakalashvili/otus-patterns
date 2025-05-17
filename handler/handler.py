from loguru import logger
from command import CommandWriteToLog, CommandRepeatOnce
from interface import ICommand


class BaseHandler(ICommand):
    def __init__(self, command: ICommand, exception: Exception, event_loop: object):
        self._command = command
        self._exception = exception
        self._event_loop = event_loop

    def execute(self):
        print(f"{self.__class__.__name__}: handle")


class DefaultHandler(BaseHandler):
    pass


class Handler1(BaseHandler):
    pass


class Handler2(BaseHandler):
    pass


class Handler3(BaseHandler):
    pass


class Handler4(BaseHandler):
    def execute(self):
        self._event_loop.add_command(
            CommandWriteToLog(logger=logger, exception=self._exception)
        )


class HandlerWriteToLog(BaseHandler):
    def execute(self):
        self._event_loop.add_command(
            CommandWriteToLog(logger=logger, exception=self._exception)
        )


class HandlerRepeaterCommand(BaseHandler):
    def execute(self):
        self._event_loop.add_command(
            CommandRepeatOnce(command=self._command, event_loop=self._event_loop)
        )


class HandlerRepeaterCommandWithStrategy(BaseHandler):
    """Хендлер исключений, реализующий стратегии"""

    def __init__(self, command: ICommand, exception: Exception, event_loop: object):
        self.strategy = None
        super().__init__(command, exception, event_loop)


class HandlerStrategyRepeatOnce(BaseHandler):
    """Повторить команду, затем записать в лог"""

    def __init__(self, command: ICommand, exception: Exception, event_loop: object):
        self.strategy = [
            # HandlerRepeaterCommand,
            HandlerWriteToLog
        ]
        super().__init__(command, exception, event_loop)


class HandlerStrategyRepeatTwice(BaseHandler):
    """Повторить команду 2 раза, затем записать в лог"""

    def __init__(self, command: ICommand, exception: Exception, event_loop: object):
        self.strategy = [
            # HandlerRepeaterCommand,
            HandlerRepeaterCommand,
            HandlerWriteToLog,
        ]
        super().__init__(command, exception, event_loop)
