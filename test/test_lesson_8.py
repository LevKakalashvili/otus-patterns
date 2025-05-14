import pytest
from mock import Mock
from collections import deque

from handler import HandlerRepeaterCommand
from handler.handler import HandlerRepeaterCommandBase, HandlerRepeaterCommandTwice
from main import main_exception_handler
from interface import ICommand
from main import main as run_main
from utils import init_queue
from main import app_queue
from command import Command1, Command2, Command3, Command4, Command4Exception
import settings


def test_once_exception(capfd, failing_command_factory):
    fail_command = failing_command_factory(1)
    commands: list[ICommand] = [Command1(), Command2(), Command3(), fail_command]

    # добавляем хэндлер, для тестовой команды
    settings.__HANDLERS_MAPPING[commands[-1].__class__] = {
        Command4Exception: [
            HandlerRepeaterCommand,
        ]
    }

    app_queue.clear()
    app_queue.extend(deque(commands))

    # Запускаем основной цикл
    run_main()

    # Проверяем поведение
    out, _ = capfd.readouterr()
    assert "Command1: execute" in out
    assert "Command2: execute" in out
    assert "Command3: execute" in out
    assert "Command4: execute" in out
    assert "Создание эксепшена попытка - 1" in out
    assert (
        f"CommandRepeatOnce: ставим {fail_command.__class__.__name__} в очередь" in out
    )


def test_twice_exception(capfd, failing_command_factory):
    assert True
