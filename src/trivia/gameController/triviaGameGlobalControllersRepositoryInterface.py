from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class TriviaGameGlobalControllersRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def addController(self, userId: str):
        pass

    @abstractmethod
    async def getControllers(self) -> frozenset[str]:
        pass

    @abstractmethod
    async def removeController(self, userId: str):
        pass
