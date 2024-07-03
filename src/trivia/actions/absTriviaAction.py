from abc import ABC, abstractmethod
from typing import Any

from .triviaActionType import TriviaActionType
from ...misc import utils as utils


class AbsTriviaAction(ABC):

    def __init__(self, actionId: str):
        if not utils.isValidStr(actionId):
            raise TypeError(f'actionId argument is malformed: \"{actionId}\"')

        self.__actionId: str = actionId

    @property
    def actionId(self) -> str:
        return self.__actionId

    @property
    @abstractmethod
    def triviaActionType(self) -> TriviaActionType:
        pass

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionId': self.__actionId,
            'triviaActionType': self.triviaActionType
        }
