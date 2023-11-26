import random
import string
from abc import ABC

from trivia.triviaActionType import TriviaActionType


class AbsTriviaAction(ABC):

    def __init__(
        self,
        triviaActionType: TriviaActionType
    ):
        if not isinstance(triviaActionType, TriviaActionType):
            raise ValueError(f'triviaActionType argument is malformed: \"{triviaActionType}\"')

        self.__triviaActionType: TriviaActionType = triviaActionType

        self.__actionId: str = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))

    def getActionId(self) -> str:
        return self.__actionId

    def getTriviaActionType(self) -> TriviaActionType:
        return self.__triviaActionType
