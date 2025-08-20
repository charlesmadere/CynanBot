from abc import ABC, abstractmethod
from typing import Any, Collection

from frozenlist import FrozenList

from ..models.chatterTimeoutHistoryEntry import ChatterTimeoutHistoryEntry


class ChatterTimeoutHistoryMapperInterface(ABC):

    @abstractmethod
    async def parseHistoryEntries(
        self,
        jsonString: str | Any | None,
    ) -> FrozenList[ChatterTimeoutHistoryEntry]:
        pass

    @abstractmethod
    async def requireHistoryEntry(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> ChatterTimeoutHistoryEntry:
        pass

    @abstractmethod
    async def serializeHistoryEntries(
        self,
        historyEntries: Collection[ChatterTimeoutHistoryEntry] | Any | None,
    ) -> str | None:
        pass

    @abstractmethod
    async def serializeHistoryEntry(
        self,
        historyEntry: ChatterTimeoutHistoryEntry,
    ) -> dict[str, Any]:
        pass
