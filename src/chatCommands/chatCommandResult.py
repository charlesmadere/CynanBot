from enum import Enum, auto


class ChatCommandResult(Enum):

    CONSUMED = auto()
    HANDLED = auto()
    IGNORED = auto()
