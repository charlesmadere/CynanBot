from abc import ABC, abstractmethod

from frozenlist import FrozenList

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from .triviaGameGlobalController import TriviaGameGlobalController
from ...misc.clearable import Clearable


class TriviaGameGlobalControllersRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def addController(
        self,
        userName: str,
    ) -> AddTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getControllers(self) -> FrozenList[TriviaGameGlobalController]:
        pass

    @abstractmethod
    async def removeController(
        self,
        userName: str,
    ) -> RemoveTriviaGameControllerResult:
        pass
