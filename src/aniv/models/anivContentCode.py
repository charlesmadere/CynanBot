from enum import Enum, auto


class AnivContentCode(Enum):

    CONTAINS_BANNED_CONTENT = auto()
    CONTAINS_URL = auto()
    IS_NONE_OR_EMPTY_OR_BLANK = auto()
    OK = auto()
