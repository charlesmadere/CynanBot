from enum import Enum, auto


class TriviaContentCode(Enum):

    ANSWER_TOO_LONG = auto()
    CONTAINS_BANNED_CONTENT = auto()
    CONTAINS_EMPTY_STR = auto()
    CONTAINS_URL = auto()
    ILLEGAL_TRIVIA_TYPE = auto()
    IS_BANNED = auto()
    IS_NONE = auto()
    OK = auto()
    QUESTION_TOO_LONG = auto()
    REPEAT = auto()
    TOO_FEW_MULTIPLE_CHOICE_RESPONSES = auto()
