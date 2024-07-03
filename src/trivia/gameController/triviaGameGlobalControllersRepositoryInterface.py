from abc import ABC, abstractmethod

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from .triviaGameGlobalController import TriviaGameGlobalController


class TriviaGameGlobalControllersRepositoryInterface(ABC):

    @abstractmethod
    async def addController(self, userName: str) -> AddTriviaGameControllerResult:
        pass

    @abstractmethod
    async def getControllers(self) -> list[TriviaGameGlobalController]:
        pass

    @abstractmethod
    async def removeController(self, userName: str) -> RemoveTriviaGameControllerResult:
        pass
