from collections import deque

from command import Command1, Command2, Command3, Command4

COMMANDS = [
    Command4(),
    Command1(),
    Command2(),
    Command3(),
]


def init_queue() -> deque:
    queue = deque(COMMANDS)
    return queue


def adapter_key(interface_cls, prop_or_method, suffix):
    base = f"{interface_cls.__module__}.{interface_cls.__name__}:{prop_or_method}"
    if suffix:
        return f"{base}.{suffix}"
    else:
        return base
