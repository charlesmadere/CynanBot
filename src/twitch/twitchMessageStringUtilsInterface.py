from abc import ABC, abstractmethod
from typing import Any


class TwitchMessageStringUtilsInterface(ABC):

    @abstractmethod
    async def getUserNameFromMessage(self, message: str | Any | None) -> str | None:
        pass

    @abstractmethod
    async def getUserNameFromCheerMessage(self, message: str | Any | None) -> str | None:
        pass

    @abstractmethod
    async def removeCheerStrings(self, message: str, repl: str = ' ') -> str:
        pass
