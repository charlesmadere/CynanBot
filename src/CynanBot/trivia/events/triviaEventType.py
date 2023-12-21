from enum import Enum, auto


class TriviaEventType(Enum):

    CLEARED_SUPER_TRIVIA_QUEUE = auto()
    CORRECT_ANSWER = auto()
    GAME_ALREADY_IN_PROGRESS = auto()
    GAME_FAILED_TO_FETCH_QUESTION = auto()
    GAME_NOT_READY = auto()
    GAME_OUT_OF_TIME = auto()
    INCORRECT_ANSWER = auto()
    INCORRECT_SUPER_ANSWER = auto()
    INVALID_ANSWER_INPUT = auto()
    NEW_GAME = auto()
    NEW_QUEUED_SUPER_GAME = auto()
    NEW_SUPER_GAME = auto()
    SUPER_GAME_ALREADY_IN_PROGRESS = auto()
    SUPER_GAME_CORRECT_ANSWER = auto()
    SUPER_GAME_FAILED_TO_FETCH_QUESTION = auto()
    SUPER_GAME_OUT_OF_TIME = auto()
    SUPER_GAME_NOT_READY = auto()
    WRONG_USER = auto()
