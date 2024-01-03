from enum import Enum, auto


class AnivContentCode(Enum):

    ATTEMPTS_COMMAND_USE = auto()
    CONTAINS_BANNED_CONTENT = auto()
    CONTAINS_URL = auto()
    IS_NONE_OR_EMPTY_OR_BLANK = auto()
    OK = auto()
    OPEN_PAREN = auto()
    OPEN_QUOTES = auto()
