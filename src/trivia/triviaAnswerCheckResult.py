from enum import Enum, auto


class TriviaAnswerCheckResult(Enum):

    CORRECT = auto()
    INCORRECT = auto()
    INVALID_INPUT = auto()
