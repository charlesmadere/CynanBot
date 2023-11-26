from enum import Enum, auto


class TriviaActionType(Enum):

    CHECK_ANSWER = auto()
    CHECK_SUPER_ANSWER = auto()
    CLEAR_SUPER_TRIVIA_QUEUE = auto()
    START_NEW_GAME = auto()
    START_NEW_SUPER_GAME = auto()
