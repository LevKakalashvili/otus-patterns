from collections import deque

from handler import DefaultHandler, BaseHandler
from interface import ICommand
from settings import get_handler_mapping


class MainExceptionHandler:
    """Главный и единственный обработчик исключений"""

    def __init__(self, app_queue: deque):
        self._mapping = get_handler_mapping()
        self._queue = app_queue

    def handle(self, command: ICommand, exception: Exception) -> ICommand:
        handlers: list[BaseHandler] = self._mapping.get(type(command), {}).get(
            type(exception),
            [
                DefaultHandler,
            ],
        )
        # Выполняем код хэндлера
        for handler in handlers:
            handler(command=command, exception=exception, queue=self._queue).execute()
