from abc import ABC, abstractmethod

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from ...misc.clearable import Clearable


class TriviaGameControllersRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def addController(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> AddTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getControllers(
        self,
        twitchChannelId: str,
    ) -> frozenset[str]:
        pass

    @abstractmethod
    async def removeController(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> RemoveTriviaGameControllerResult:
        pass
