from abc import ABC, abstractmethod
from typing import Any

from CynanBot.cheerActions.timeout.timeoutCheerActionEntry import \
    TimeoutCheerActionEntry


class TimeoutCheerActionJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTimeoutCheerActionEntriesString(
        self,
        jsonString: str | Any | None
    ) -> list[TimeoutCheerActionEntry] | None:
        pass

    @abstractmethod
    async def parseTimeoutCheerActionEntry(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TimeoutCheerActionEntry | None:
        pass

    @abstractmethod
    async def serializeTimeoutCheerActionEntriesToJsonString(
        self,
        entries: list[TimeoutCheerActionEntry] | None
    ) -> str | None:
        pass

    @abstractmethod
    async def serializeTimeoutCheerActionEntry(
        self,
        entry: TimeoutCheerActionEntry | None
    ) -> dict[str, Any] | None:
        pass
