import pytest
from command import Command4, Command4Exception


class FailingNtimesCommand4(Command4):
    """Команда Command4 (только для тестов), которая падает N раз, а затем успешно выполняется."""

    def __init__(self, fail_count: int):
        super().__init__()
        self.fail_count = fail_count

    def execute(self):
        if self.fail_count > 0:
            msg = f"Создание эксепшена попытка - {self.fail_count}"
            print(msg)
            self.fail_count -= 1
            raise Command4Exception(msg)
        super().execute()


@pytest.fixture
def failing_command_factory():
    def _factory(fail_count: int) -> FailingNtimesCommand4:
        return FailingNtimesCommand4(fail_count)

    return _factory
