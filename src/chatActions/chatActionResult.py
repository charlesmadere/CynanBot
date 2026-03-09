from enum import Enum, auto


class ChatActionResult(Enum):

    CONSUMED = auto()
    HANDLED = auto()
    IGNORED = auto()
