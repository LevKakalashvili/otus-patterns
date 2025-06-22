import queue
import threading
import time
from typing import Optional

from handler import MainExceptionHandler
from interface import ICommand


class ThreadedCommandExecutor:
    def __init__(self):
        self._queue = queue.Queue()
        self._stop_event = threading.Event()
        self._soft_stop = False
        self._thread: Optional[threading.Thread] = None
        self._exception_handler = MainExceptionHandler(event_loop=self)
        self._errors = []

    def add_command(self, command: ICommand) -> None:
        self._queue.put(command)

    def _run(self):
        while not self._stop_event.is_set() or (self._soft_stop and not self._queue.empty()):
            try:
                command = self._queue.get(timeout=0.1)
                try:
                    command.execute()
                except Exception as exc:
                    self._errors.append((command, exc))
                    self._exception_handler.handle(command, exc)
            except queue.Empty:
                time.sleep(0.1)

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._soft_stop = False
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def hard_stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()

    def soft_stop(self):
        self._soft_stop = True
        self._stop_event.set()
        if self._thread:
            self._thread.join()

    def is_alive(self):
        return self._thread is not None and self._thread.is_alive()

    def get_errors(self):
        return self._errors


class StartCommand(ICommand):
    def __init__(self, executor: ThreadedCommandExecutor):
        self.executor = executor

    def execute(self):
        self.executor.start()


class HardStopCommand(ICommand):
    def __init__(self, executor: ThreadedCommandExecutor):
        self.executor = executor

    def execute(self):
        self.executor.hard_stop()


class SoftStopCommand(ICommand):
    def __init__(self, executor: ThreadedCommandExecutor):
        self.executor = executor

    def execute(self):
        self.executor.soft_stop()
