from ioc.ioc_container import Executable, IoC
from ioc.const import IOC_COMMAND, SCOPE
import threading

class MoveCommand(Executable):
    def __init__(self, obj_to_move):
        super().__init__(lambda: print(f"Moving {obj_to_move}"))


def test_register_and_resolve():
    IoC.resolve(
        IOC_COMMAND.REGISTER.value,
        "test_cmd",
        lambda args: Executable(lambda: print(f"Run with {args[0]}")),
    ).execute()
    cmd = IoC.resolve("test_cmd", "arg1")
    cmd.execute()


def test_scopes():
    IoC.resolve(SCOPE.NEW.value, "test").execute()
    IoC.resolve(SCOPE.CURRENT.value, "test").execute()
    IoC.resolve(IOC_COMMAND.REGISTER.value, "x", lambda args: "Scoped!").execute()
    assert IoC.resolve("x") == "Scoped!"


def worker(scope_id, value):
    IoC.resolve(SCOPE.NEW.value, scope_id).execute()
    IoC.resolve(SCOPE.CURRENT.value, scope_id).execute()
    IoC.resolve(IOC_COMMAND.REGISTER.value, "val", lambda args: value).execute()
    assert IoC.resolve("val") == value


def test_threads():
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(f"scope_{i}", i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    print("--- test_register_and_resolve ---")
    test_register_and_resolve()

    print("--- test_scopes ---")
    test_scopes()
    print("Scopes test passed")

    print("--- test_threads ---")
    test_threads()
    print("Threads test passed")
