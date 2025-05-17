from collections import defaultdict

from handler import DefaultHandler
from interface import ICommand
from settings import get_handler_mapping


class MainExceptionHandler:
    """Главный и единственный обработчик исключений"""

    def __init__(self, event_loop):
        self._mapping = get_handler_mapping()
        self._event_loop = event_loop
        self._exception_strategy: dict[int, list[ICommand]] = defaultdict(list)

    def handle(self, command: ICommand, exception: Exception) -> None:
        """Хендлер исключений"""
        command_type = type(command)
        exception_type = type(exception)
        command_id = id(command)

        handlers = self._mapping.get(command_type, {}).get(
            exception_type, [DefaultHandler]
        )

        for handler_cls in handlers:
            handler = handler_cls(
                command=command, exception=exception, event_loop=self._event_loop
            )

            # Есть ли стратегия для повторов
            if self._exception_strategy.get(command_id):
                handler = self._exception_strategy[command_id].pop(0)
            else:
                strategy = getattr(handler, "strategy", None)
                if strategy:
                    self._exception_strategy[command_id].extend(
                        h_cls(
                            command=command,
                            exception=exception,
                            event_loop=self._event_loop,
                        )
                        for h_cls in strategy
                    )
                    handler = self._exception_strategy[command_id].pop(0)

            handler.execute()

    def clear_queue(self):
        """Очистка очереди стратегий от команд, которых уже нет в общем loop-е"""

        # Чистим пустые стратегии
        for command_id in list(self._exception_strategy.keys()):
            if not self._exception_strategy[command_id]:
                del self._exception_strategy[command_id]
