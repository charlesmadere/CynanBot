from abc import ABC, abstractmethod
from typing import Any

from .triviaEventType import TriviaEventType
from ...misc import utils as utils


class AbsTriviaEvent(ABC):

    def __init__(
        self,
        actionId: str,
        eventId: str
    ):
        if not utils.isValidStr(actionId):
            raise TypeError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(eventId):
            raise TypeError(f'eventId argument is malformed: \"{eventId}\"')

        self.__actionId: str = actionId
        self.__eventId: str = eventId

    def getActionId(self) -> str:
        return self.__actionId

    def getEventId(self) -> str:
        return self.__eventId

    @abstractmethod
    def getTriviaEventType(self) -> TriviaEventType:
        pass

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionId': self.__actionId,
            'eventId': self.__eventId,
            'triviaEventType': self.getTriviaEventType()
        }
