from typing import Callable, Any
import threading
from .const import SCOPE, IOC_COMMAND


class Executable:
    def __init__(self, action: Callable[[], None]):
        self._action = action

    def execute(self) -> None:
        self._action()


class IoC:
    _global_scope = {}
    _scopes = threading.local()

    @staticmethod
    def _get_current_scope() -> dict:
        if not hasattr(IoC._scopes, "current"):
            IoC._scopes.current = IoC._global_scope
        return IoC._scopes.current

    @staticmethod
    def resolve(key: str, *args: Any) -> Any:
        if key == IOC_COMMAND.REGISTER.value:
            reg_key, factory = args
            IoC._get_current_scope()[reg_key] = factory
            return Executable(lambda: None)

        elif key == SCOPE.NEW.value:
            scope_id = args[0]
            IoC._global_scope[scope_id] = {}
            return Executable(lambda: None)

        elif key == SCOPE.CURRENT.value:
            scope_id = args[0]
            IoC._scopes.current = IoC._global_scope.get(scope_id, IoC._global_scope)
            return Executable(lambda: None)

        factory = IoC._get_current_scope().get(key)
        if not factory:
            raise KeyError(f"Dependency not found for key: {key}")
        return factory(args)
