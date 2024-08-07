from enum import Enum, auto


class OpenTriviaDatabaseResponseCode(Enum):

    INVALID_PARAMETER = auto()
    NO_RESULTS = auto()
    RATE_LIMIT = auto()
    SUCCESS = auto()
    TOKEN_EMPTY = auto()
    TOKEN_NOT_FOUND = auto()
