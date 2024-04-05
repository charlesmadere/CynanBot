from abc import ABC, abstractmethod

from CynanBot.trivia.banned.addBannedTriviaGameControllerResult import \
    AddBannedTriviaGameControllerResult
from CynanBot.trivia.banned.bannedTriviaGameController import \
    BannedTriviaGameController
from CynanBot.trivia.gameController.removeBannedTriviaGameControllerResult import \
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
