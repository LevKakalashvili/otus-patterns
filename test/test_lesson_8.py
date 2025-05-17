from handler import HandlerStrategyRepeatTwice, HandlerStrategyRepeatOnce
from interface import ICommand
from event_loop.event_loop import EventLoop
from command import Command4Exception
import settings


def test_once_exception(capfd, failing_command_factory):
    fail_command = failing_command_factory(1)

    # добавляем хэндлер, для тестовой команды
    settings.__HANDLERS_MAPPING[fail_command.__class__] = {
        Command4Exception: [
            HandlerStrategyRepeatOnce,
        ]
    }

    # Запускаем основной цикл
    event_loop = EventLoop()
    for command in [fail_command]:
        event_loop.add_command(command)
    event_loop.run()

    # Проверяем поведение
    out, _ = capfd.readouterr()
    assert "Создание эксепшена попытка - 1" in out
    assert (
        f"CommandRepeatOnce: ставим {fail_command.__class__.__name__} в очередь" in out
    )
    assert "CommandWriteToLog: execute" in out


def test_twice_exception(capfd, failing_command_factory):
    fail_command = failing_command_factory(2)
    commands: list[ICommand] = [fail_command]

    # добавляем хэндлер, для тестовой команды
    settings.__HANDLERS_MAPPING[commands[-1].__class__] = {
        Command4Exception: [
            HandlerStrategyRepeatTwice,
        ]
    }

    # Запускаем основной цикл
    event_loop = EventLoop()
    for command in [fail_command]:
        event_loop.add_command(command)
    event_loop.run()

    # Проверяем поведение
    out, _ = capfd.readouterr()
    assert "Создание эксепшена попытка - 1" in out
    assert "Создание эксепшена попытка - 2" in out
    assert (
        f"CommandRepeatOnce: ставим {fail_command.__class__.__name__} в очередь" in out
    )
    assert "CommandWriteToLog: execute" in out
