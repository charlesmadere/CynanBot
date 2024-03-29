from abc import ABC, abstractmethod
from typing import List

from CynanBot.trivia.gameController.addTriviaGameControllerResult import \
    AddTriviaGameControllerResult
from CynanBot.trivia.gameController.triviaGameController import \
    TriviaGameController
from CynanBot.trivia.gameController.removeTriviaGameControllerResult import \
    RemoveTriviaGameControllerResult


class TriviaGameControllersRepositoryInterface(ABC):

    @abstractmethod
    async def addController(
        self,
        twitchChannel: str,
        userName: str
    ) -> AddTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getControllers(self, twitchChannel: str) -> List[TriviaGameController]:
        pass

    @abstractmethod
    async def removeController(
        self,
        twitchChannel: str,
        userName: str
    ) -> RemoveTriviaGameControllerResult:
        pass
