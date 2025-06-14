import time

from event_loop.event_loop_thread import (
    HardStopCommand,
    SoftStopCommand,
    StartCommand,
    ThreadedCommandExecutor,
)
from interface import ICommand


class DummyCommand(ICommand):
    def __init__(self, delay=0.1, should_fail=False):
        self.executed = False
        self.delay = delay
        self.should_fail = should_fail

    def execute(self):
        time.sleep(self.delay)
        if self.should_fail:
            raise RuntimeError("Command failed")
        self.executed = True


class FailingCommand(ICommand):
    def __init__(self):
        self.executed = False

    def execute(self):
        self.executed = True
        raise ValueError("Deliberate failure")


class SuccessCommand(ICommand):
    def __init__(self):
        self.executed = False

    def execute(self):
        self.executed = True


def test_start_command():
    executor = ThreadedCommandExecutor()
    start_cmd = StartCommand(executor)
    start_cmd.execute()
    time.sleep(0.2)
    assert executor.is_alive()


def test_hard_stop_command():
    executor = ThreadedCommandExecutor()
    executor.start()
    time.sleep(0.1)
    stop_cmd = HardStopCommand(executor)
    stop_cmd.execute()
    assert not executor.is_alive()


def test_soft_stop_command():
    executor = ThreadedCommandExecutor()
    cmd1 = DummyCommand(delay=0.2)
    cmd2 = DummyCommand(delay=0.2)
    executor.add_command(cmd1)
    executor.add_command(cmd2)
    executor.start()
    time.sleep(0.1)
    stop_cmd = SoftStopCommand(executor)
    stop_cmd.execute()
    assert cmd1.executed and cmd2.executed
    assert not executor.is_alive()


def test_error_handling_and_continue():
    executor = ThreadedCommandExecutor()
    fail_cmd = FailingCommand()
    success_cmd = SuccessCommand()
    executor.add_command(fail_cmd)
    executor.add_command(success_cmd)
    executor.start()
    time.sleep(0.2)
    SoftStopCommand(executor).execute()
    assert fail_cmd.executed
    assert success_cmd.executed
    assert len(executor.get_errors()) == 1
    assert isinstance(executor.get_errors()[0][1], ValueError)
