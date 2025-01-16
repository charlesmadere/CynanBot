from enum import Enum, auto


class ContentCode(Enum):

    CONTAINS_BANNED_CONTENT = auto()
    CONTAINS_URL = auto()
    IS_BLANK = auto()
    IS_EMPTY = auto()
    IS_NONE = auto()
    OK = auto()
