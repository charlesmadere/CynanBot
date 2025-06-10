from abc import ABC, abstractmethod
from typing import Any, Final

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

        self.__actionId: Final[str] = actionId
        self.__eventId: Final[str] = eventId

    @property
    def actionId(self) -> str:
        return self.__actionId

    @property
    def eventId(self) -> str:
        return self.__eventId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionId': self.__actionId,
            'eventId': self.__eventId,
            'triviaEventType': self.triviaEventType
        }

    @property
    @abstractmethod
    def triviaEventType(self) -> TriviaEventType:
        pass
