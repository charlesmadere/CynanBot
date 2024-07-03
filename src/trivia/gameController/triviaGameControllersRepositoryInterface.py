from abc import ABC, abstractmethod

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from .triviaGameController import TriviaGameController


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
