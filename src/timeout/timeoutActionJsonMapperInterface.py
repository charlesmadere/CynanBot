from abc import ABC, abstractmethod
from typing import Any

from frozenlist import FrozenList

from .timeoutActionHistoryEntry import TimeoutActionHistoryEntry


class TimeoutActionJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTimeoutActionEntriesString(
        self,
        jsonString: str | Any | None
    ) -> FrozenList[TimeoutActionHistoryEntry] | None:
        pass

    @abstractmethod
    async def parseTimeoutActionEntry(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TimeoutActionHistoryEntry | None:
        pass

    @abstractmethod
    async def serializeTimeoutActionEntriesToJsonString(
        self,
        entries: list[TimeoutActionHistoryEntry] | None
    ) -> str | None:
        pass

    @abstractmethod
    async def serializeTimeoutActionEntry(
        self,
        entry: TimeoutActionHistoryEntry | None
    ) -> dict[str, Any] | None:
        pass
