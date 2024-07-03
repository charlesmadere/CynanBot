from enum import Enum, auto


class RemoveTriviaGameControllerResult(Enum):

    DOES_NOT_EXIST = auto()
    ERROR = auto()
    REMOVED = auto()
