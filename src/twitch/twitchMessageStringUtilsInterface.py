from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class TwitchMessageStringUtilsInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class ParsedUserNameCommandMessage:
        command: str
        rawMessage: str
        remainingMessage: str | None
        userName: str

    @abstractmethod
    async def getUserNameFromMessage(self, message: str | Any | None) -> str | None:
        pass

    @abstractmethod
    async def getUserNameFromCheerMessage(self, message: str | Any | None) -> str | None:
        pass

    @abstractmethod
    async def parseUserNameCommandMessage(
        self,
        message: str | Any | None,
    ) -> ParsedUserNameCommandMessage | None:
        pass

    @abstractmethod
    async def removeCheerStrings(self, message: str, repl: str = ' ') -> str:
        pass
