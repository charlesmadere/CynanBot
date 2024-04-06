from abc import ABC, abstractmethod

from CynanBot.trivia.gameController.addTriviaGameControllerResult import \
    AddTriviaGameControllerResult
from CynanBot.trivia.gameController.removeTriviaGameControllerResult import \
    RemoveTriviaGameControllerResult
from CynanBot.trivia.gameController.triviaGameGlobalController import \
    TriviaGameGlobalController


class TriviaGameGlobalControllersRepositoryInterface(ABC):

    @abstractmethod
    async def addController(self, userName: str) -> AddTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getControllers(self) -> list[TriviaGameGlobalController]:
        pass

    @abstractmethod
    async def removeController(self, userName: str) -> RemoveTriviaGameControllerResult:
        pass
