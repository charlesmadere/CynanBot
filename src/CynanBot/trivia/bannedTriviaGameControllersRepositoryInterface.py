from abc import ABC, abstractmethod
from typing import List

from trivia.addBannedTriviaGameControllerResult import \
    AddBannedTriviaGameControllerResult
from trivia.bannedTriviaGameController import BannedTriviaGameController
from trivia.removeBannedTriviaGameControllerResult import \
    RemoveBannedTriviaGameControllerResult


class BannedTriviaGameControllersRepositoryInterface(ABC):

    @abstractmethod
    async def addBannedController(self, userName: str) -> AddBannedTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getBannedControllers(self) -> List[BannedTriviaGameController]:
        pass

    @abstractmethod
    async def removeBannedController(self, userName: str) -> RemoveBannedTriviaGameControllerResult:
        pass
