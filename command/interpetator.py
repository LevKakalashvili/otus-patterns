from interface import ICommand
from ioc.ioc_container import IoC
from models.message import IncomingMessage


class InterpretCommand(ICommand):
    def __init__(self, message: IncomingMessage):
        self._message = message

    def execute(self):
        obj = IoC.resolve("Игровые объекты", self._message.object_id)
        IoC.resolve("Установить параметры операции", obj, self._message.args)
        cmd = IoC.resolve(self._message.operation_id, obj)
        queue = IoC.resolve("Очередь команд", self._message.game_id)
        queue.enqueue(cmd)