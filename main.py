from handler import MainExceptionHandler
from interface import ICommand
from collections import deque
from utils import init_queue

# Создаем очередь команд
app_queue: deque = init_queue()
# Создаем общий обработчик исключений
main_exception_handler: MainExceptionHandler = MainExceptionHandler(app_queue=app_queue)


def main():
    while app_queue:
        current_command: ICommand = app_queue.pop()
        try:
            current_command.execute()
        except Exception as exception:
            main_exception_handler.handle(command=current_command, exception=exception)


if __name__ == "__main__":
    main()
