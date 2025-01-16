from abc import ABC, abstractmethod

from .addBannedTriviaGameControllerResult import AddBannedTriviaGameControllerResult
from .bannedTriviaGameController import BannedTriviaGameController
from ..gameController.removeBannedTriviaGameControllerResult import \
    RemoveBannedTriviaGameControllerResult


class BannedTriviaGameControllersRepositoryInterface(ABC):

    @abstractmethod
    async def addBannedController(self, userName: str) -> AddBannedTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getBannedControllers(self) -> list[BannedTriviaGameController]:
        pass

    @abstractmethod
    async def removeBannedController(self, userName: str) -> RemoveBannedTriviaGameControllerResult:
        pass
