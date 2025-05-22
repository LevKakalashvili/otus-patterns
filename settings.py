from command import Command1, Command4, Command2, Command3
from command import (
    Command1Exception,
    Command4Exception,
    Command2Exception,
    Command3Exception,
)
from handler import Handler1, Handler4, Handler2, Handler3, HandlerRepeaterCommand

__HANDLERS_MAPPING = {
    Command1: {
        Command1Exception: [
            Handler1,
        ]
    },
    Command4: {Command4Exception: [Handler4, HandlerRepeaterCommand]},
    Command2: {
        Command2Exception: [
            Handler2,
        ]
    },
    Command3: {
        Command3Exception: [
            Handler3,
        ]
    },
}


def get_handler_mapping() -> dict:
    return __HANDLERS_MAPPING
