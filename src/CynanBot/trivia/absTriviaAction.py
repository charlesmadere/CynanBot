from abc import ABC, abstractmethod

import CynanBot.misc.utils as utils
from CynanBot.trivia.triviaActionType import TriviaActionType


class AbsTriviaAction(ABC):

    def __init__(self, actionId: str):
        if not utils.isValidStr(actionId):
            raise ValueError(f'actionId argument is malformed: \"{actionId}\"')

        self.__actionId: str = actionId

    def getActionId(self) -> str:
        return self.__actionId

    @abstractmethod
    def getTriviaActionType(self) -> TriviaActionType:
        pass
