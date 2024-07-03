from enum import Enum, auto


class RemoveBannedTriviaGameControllerResult(Enum):

    ERROR = auto()
    NOT_BANNED = auto()
    REMOVED = auto()
