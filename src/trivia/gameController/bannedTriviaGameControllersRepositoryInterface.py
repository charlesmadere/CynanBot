from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class BannedTriviaGameControllersRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def addBannedController(self, userId: str):
        pass

    @abstractmethod
    async def getBannedControllers(self) -> frozenset[str]:
        pass

    @abstractmethod
    async def removeBannedController(self, userId: str):
        pass
