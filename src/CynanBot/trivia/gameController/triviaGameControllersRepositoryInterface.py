from abc import ABC, abstractmethod

from CynanBot.trivia.gameController.addTriviaGameControllerResult import \
    AddTriviaGameControllerResult
from CynanBot.trivia.gameController.removeTriviaGameControllerResult import \
    RemoveTriviaGameControllerResult
from CynanBot.trivia.gameController.triviaGameController import \
    TriviaGameController


class TriviaGameControllersRepositoryInterface(ABC):

    @abstractmethod
    async def addController(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userName: str
    ) -> AddTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getControllers(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> list[TriviaGameController]:
        pass

    @abstractmethod
    async def removeController(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userName: str
    ) -> RemoveTriviaGameControllerResult:
        pass
