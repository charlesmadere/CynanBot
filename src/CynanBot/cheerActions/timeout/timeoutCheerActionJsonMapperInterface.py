from abc import ABC, abstractmethod
from typing import Any

from CynanBot.cheerActions.timeout.timeoutCheerActionEntry import \
    TimeoutCheerActionEntry


class TimeoutCheerActionJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTimeoutCheerActionEntry(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TimeoutCheerActionEntry | None:
        pass

    @abstractmethod
    async def parseTimeoutCheerActionEntriesString(
        self,
        string: str | Any | None
    ) -> list[TimeoutCheerActionEntry] | None:
        pass
