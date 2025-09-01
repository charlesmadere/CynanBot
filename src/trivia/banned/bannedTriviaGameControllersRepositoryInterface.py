from abc import ABC, abstractmethod

from .addBannedTriviaGameControllerResult import AddBannedTriviaGameControllerResult
from .removeBannedTriviaGameControllerResult import RemoveBannedTriviaGameControllerResult
from ...misc.clearable import Clearable


class BannedTriviaGameControllersRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def addBannedController(
        self,
        userId: str,
    ) -> AddBannedTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getBannedControllers(self) -> frozenset[str]:
        pass

    @abstractmethod
    async def removeBannedController(
        self,
        userId: str,
    ) -> RemoveBannedTriviaGameControllerResult:
        pass
