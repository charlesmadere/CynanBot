from abc import ABC, abstractmethod
from typing import List

from CynanBot.trivia.addTriviaGameControllerResult import \
    AddTriviaGameControllerResult
from CynanBot.trivia.gameController.triviaGameGlobalController import \
    TriviaGameGlobalController
from CynanBot.trivia.removeTriviaGameControllerResult import \
    RemoveTriviaGameControllerResult


class TriviaGameGlobalControllersRepositoryInterface(ABC):

    @abstractmethod
    async def addController(self, userName: str) -> AddTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getControllers(self) -> List[TriviaGameGlobalController]:
        pass

    @abstractmethod
    async def removeController(self, userName: str) -> RemoveTriviaGameControllerResult:
        pass
