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
