from abc import ABC, abstractmethod

from frozenlist import FrozenList

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from .triviaGameController import TriviaGameController
from ...misc.clearable import Clearable


class TriviaGameControllersRepositoryInterface(Clearable, ABC):

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
    ) -> FrozenList[TriviaGameController]:
        pass

    @abstractmethod
    async def removeController(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userName: str
    ) -> RemoveTriviaGameControllerResult:
        pass
