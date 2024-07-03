from enum import Enum, auto


class AddBannedTriviaGameControllerResult(Enum):

    ADDED = auto()
    ALREADY_EXISTS = auto()
    ERROR = auto()
