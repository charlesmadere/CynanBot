from abc import ABC, abstractmethod

from frozenlist import FrozenList

from .addBannedTriviaGameControllerResult import AddBannedTriviaGameControllerResult
from .bannedTriviaGameController import BannedTriviaGameController
from .removeBannedTriviaGameControllerResult import RemoveBannedTriviaGameControllerResult
from ...misc.clearable import Clearable


class BannedTriviaGameControllersRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def addBannedController(
        self,
        userName: str
    ) -> AddBannedTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getBannedControllers(self) -> FrozenList[BannedTriviaGameController]:
        pass

    @abstractmethod
    async def removeBannedController(
        self,
        userName: str
    ) -> RemoveBannedTriviaGameControllerResult:
        pass
