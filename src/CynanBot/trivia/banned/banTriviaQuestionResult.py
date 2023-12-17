from enum import Enum, auto


class BanTriviaQuestionResult(Enum):

    ALREADY_BANNED = auto()
    BANNED = auto()
    NOT_BANNED = auto()
    UNBANNED = auto()
