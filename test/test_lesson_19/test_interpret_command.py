import pytest
from unittest.mock import Mock, patch
from models.message import IncomingMessage
from command import InterpretCommand


@pytest.fixture
def test_message():
    return IncomingMessage(
        game_id="game-123",
        object_id="ship-548",
        operation_id="move_straight",
        args={"velocity": 2}
    )


@patch("command.interpetator.IoC")
def test_interpret_command_executes_command(mock_ioc, test_message):
    mock_obj = Mock()
    mock_cmd = Mock()
    mock_queue = Mock()

    # Реализация side_effect через if-else
    def resolve_side_effect(key, *args):
        if key == "Игровые объекты" and args[0] == test_message.object_id:
            return mock_obj
        elif key == "Установить параметры операции" and args[0] == mock_obj and args[
            1] == test_message.args:
            return None
        elif key == test_message.operation_id and args[0] == mock_obj:
            return mock_cmd
        elif key == "Очередь команд" and args[0] == test_message.game_id:
            return mock_queue
        raise KeyError(f"Unexpected resolve call: {key}, {args}")

    # Настройка моков
    mock_ioc.resolve.side_effect = resolve_side_effect

    # Выполнение
    cmd = InterpretCommand(test_message)
    cmd.execute()

    # Проверки
    mock_queue.enqueue.assert_called_once_with(mock_cmd)
