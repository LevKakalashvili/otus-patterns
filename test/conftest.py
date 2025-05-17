import pytest
from command import Command4, Command4Exception


class FailingNtimesCommand4(Command4):
    """Команда Command4 (только для тестов), которая падает N раз, а затем успешно выполняется."""

    def __init__(self, fail_count: int):
        super().__init__()
        self.fail_count = fail_count
        self.cnt_failed = 0

    def execute(self):
        while self.cnt_failed < self.fail_count:
            msg = f"Создание эксепшена попытка - {self.cnt_failed + 1}"
            print(msg)
            self.cnt_failed += 1
            raise Command4Exception(msg)
        super().execute()


@pytest.fixture
def failing_command_factory():
    def _factory(fail_count: int) -> FailingNtimesCommand4:
        return FailingNtimesCommand4(fail_count)

    return _factory
