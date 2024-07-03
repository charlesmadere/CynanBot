from enum import Enum, auto


class AddTriviaGameControllerResult(Enum):

    ADDED = auto()
    ALREADY_EXISTS = auto()
    ERROR = auto()
