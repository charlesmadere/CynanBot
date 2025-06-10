from abc import ABC, abstractmethod
from typing import Any, Final

from .triviaActionType import TriviaActionType
from ...misc import utils as utils


class AbsTriviaAction(ABC):

    def __init__(self, actionId: str):
        if not utils.isValidStr(actionId):
            raise TypeError(f'actionId argument is malformed: \"{actionId}\"')

        self.__actionId: Final[str] = actionId

    @property
    def actionId(self) -> str:
        return self.__actionId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionId': self.__actionId,
            'triviaActionType': self.triviaActionType
        }

    @property
    @abstractmethod
    def triviaActionType(self) -> TriviaActionType:
        pass
