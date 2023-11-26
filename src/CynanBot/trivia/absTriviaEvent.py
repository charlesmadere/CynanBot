import random
import string
from abc import ABC

import CynanBot.misc.utils as utils
from CynanBot.trivia.triviaEventType import TriviaEventType


class AbsTriviaEvent(ABC):

    def __init__(
        self,
        actionId: str,
        triviaEventType: TriviaEventType
    ):
        if not utils.isValidStr(actionId):
            raise ValueError(f'actionId argument is malformed: \"{actionId}\"')
        elif not isinstance(triviaEventType, TriviaEventType):
            raise ValueError(f'triviaEventType argument is malformed: \"{triviaEventType}\"')

        self.__actionId: str = actionId
        self.__triviaEventType: TriviaEventType = triviaEventType

        self.__eventId: str = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))

    def getActionId(self) -> str:
        return self.__actionId

    def getEventId(self) -> str:
        return self.__eventId

    def getTriviaEventType(self) -> TriviaEventType:
        return self.__triviaEventType
