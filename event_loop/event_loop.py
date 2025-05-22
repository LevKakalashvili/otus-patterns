from handler import MainExceptionHandler
from interface import ICommand
from collections import deque


class EventLoop:
    def __init__(self):
        self.queue: deque[ICommand] = deque()
        self.exception_handler = MainExceptionHandler(event_loop=self)

    def add_command(self, command: ICommand) -> None:
        self.queue.appendleft(command)

    def run(self) -> None:
        while self.queue:
            command: ICommand = self.queue.pop()
            try:
                command.execute()
            except Exception as exc:
                self.exception_handler.handle(command, exc)
