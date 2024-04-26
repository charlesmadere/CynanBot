from abc import ABC, abstractmethod

from asyncio import AbstractEventLoop
from typing import Coroutine


class BackgroundTaskHelperInterface(ABC):

    @abstractmethod
    def createTask(self, coro: Coroutine):
        pass

    @abstractmethod
    def getEventLoop(self) -> AbstractEventLoop:
        pass
