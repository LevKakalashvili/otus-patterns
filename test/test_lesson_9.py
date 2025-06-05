from unittest.mock import Mock

import pytest
from command import (
    CommandCheckFuel,
    CommandException,
    StarShipFuelSystem,
    CommandBurnFuel,
    MacroCommand,
    CommandMoveWithFuel,
    CommandChangeVelocity,
    CommandRotateWithVelocityChange,
)
from interface import ICommand


class TestCommand(ICommand):
    def __init__(self):
        self.executed = False

    def execute(self):
        self.executed = True


class TestMovableObject:
    def __init__(self):
        self.moved = False

    def move(self):
        self.moved = True


class TestCommandMove:
    def __init__(self, obj):
        self._obj = obj

    def execute(self):
        self._obj.move()


class TestFailingCommand(ICommand):
    def execute(self):
        raise CommandException("Команда завершилась с ошибкой")


def test_check_fuel_command_success():
    fuel_system = StarShipFuelSystem(initial_fuel=100)
    command = CommandCheckFuel(fuel_system=fuel_system, required_fuel=50)
    command.execute()


def test_check_fuel_command_failed():
    fuel_system = StarShipFuelSystem(initial_fuel=100)
    command = CommandCheckFuel(fuel_system=fuel_system, required_fuel=200)

    with pytest.raises(CommandException, match="Недостаточно топлива"):
        command.execute()


def test_burn_fuel_command_success():
    fuel_system = StarShipFuelSystem(initial_fuel=100)
    command = CommandBurnFuel(fuel_system=fuel_system, burn_amount=40)
    command.execute()
    assert fuel_system.get_fuel_level() == 60


def test_burn_fuel_command_exact_amount():
    fuel_system = StarShipFuelSystem(initial_fuel=50)
    command = CommandBurnFuel(fuel_system=fuel_system, burn_amount=50)
    command.execute()
    assert fuel_system.get_fuel_level() == 0


def test_burn_fuel_command_raises_if_insufficient():
    fuel_system = StarShipFuelSystem(initial_fuel=20)
    command = CommandBurnFuel(fuel_system=fuel_system, burn_amount=30)
    with pytest.raises(CommandException, match="У нашего корабля закончилось топливо"):
        command.execute()


def test_macro_command_success():
    cmd1 = TestCommand()
    cmd2 = TestCommand()
    macro = MacroCommand([cmd1, cmd2])
    macro.execute()

    assert cmd1.executed
    assert cmd2.executed


def test_macro_command_stops_on_exception():
    cmd1 = TestCommand()
    cmd2 = TestFailingCommand()
    cmd3 = TestCommand()
    macro = MacroCommand([cmd1, cmd2, cmd3])

    with pytest.raises(CommandException, match="Команда завершилась с ошибкой"):
        macro.execute()

    assert cmd1.executed
    assert not hasattr(cmd3, "executed") or not cmd3.executed


def test_move_with_fuel_success(monkeypatch):
    # Мокаем топливную систему — топлива не хватает
    fuel_system = Mock()
    fuel_system.get_fuel_level.return_value = 50

    movable = Mock()

    # Подмена CommandMove внутри модуля command
    import command

    monkeypatch.setattr(command, "CommandMove", lambda obj: TestCommandMove(obj))

    cmd = CommandMoveWithFuel(fuel_system, required_fuel=10, obj_to_move=movable)
    cmd.execute()

    fuel_system.get_fuel_level.assert_called_once()
    fuel_system.consume.assert_called_once_with(10)
    movable.move.assert_called_once()


def test_move_with_fuel_fails_on_low_fuel(monkeypatch):
    # Мокаем топливную систему — топлива не хватает
    fuel_system = Mock()
    fuel_system.get_fuel_level.return_value = 5  # меньше требуемого

    movable = Mock()

    # Подмена CommandMove внутри модуля command
    import command

    monkeypatch.setattr(command, "CommandMove", lambda obj: TestCommandMove(obj))

    command = CommandMoveWithFuel(
        fuel_system=fuel_system, required_fuel=10, obj_to_move=movable
    )

    with pytest.raises(CommandException, match="Недостаточно топлива"):
        command.execute()

    # Убедимся, что движение и сжигание топлива не происходили
    movable.move.assert_not_called()
    fuel_system.consume.assert_not_called()


def test_change_velocity_when_object_is_moving():
    obj = Mock()
    obj.is_moving.return_value = True

    command = CommandChangeVelocity(obj)
    command.execute()

    obj.is_moving.assert_called_once()
    obj.adjust_velocity.assert_called_once()


def test_change_velocity_when_object_is_not_moving():
    obj = Mock()
    obj.is_moving.return_value = False

    command = CommandChangeVelocity(obj)
    command.execute()

    obj.is_moving.assert_called_once()
    obj.adjust_velocity.assert_not_called()


def test_rotate_and_adjust_velocity_when_moving():
    # поворот + изменение вектора, если объект движется
    obj = Mock()
    obj.is_moving.return_value = True

    command = CommandRotateWithVelocityChange(obj)
    command.execute()

    obj.rotate.assert_called_once()
    obj.is_moving.assert_called_once()
    obj.adjust_velocity.assert_called_once()


def test_rotate_without_adjust_velocity_when_stationary():
    # поворот происходит, а изменение вектора — нет
    obj = Mock()
    obj.is_moving.return_value = False

    command = CommandRotateWithVelocityChange(obj)
    command.execute()

    obj.rotate.assert_called_once()
    obj.is_moving.assert_called_once()
    obj.adjust_velocity.assert_not_called()
