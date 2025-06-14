from enum import Enum


class IOC_COMMAND(str, Enum):
    REGISTER = "IoC.Register"


class SCOPE(str, Enum):
    NEW = "Scopes.New"
    CURRENT = "Scopes.Current"
