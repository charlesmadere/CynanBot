from abc import ABC, abstractmethod

import CynanBot.misc.utils as utils
from CynanBot.trivia.events.triviaEventType import TriviaEventType


class AbsTriviaEvent(ABC):

    def __init__(
        self,
        actionId: str,
        eventId: str
    ):
        if not utils.isValidStr(actionId):
            raise ValueError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(eventId):
            raise ValueError(f'eventId argument is malformed: \"{eventId}\"')

        self.__actionId: str = actionId
        self.__eventId: str = eventId

    def getActionId(self) -> str:
        return self.__actionId

    def getEventId(self) -> str:
        return self.__eventId

    @abstractmethod
    def getTriviaEventType(self) -> TriviaEventType:
        pass
