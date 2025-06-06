from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class EccoResponseParserInterface(ABC):

    @abstractmethod
    async def findTimerDateTimeValue(
        self,
        scriptString: str | Any | None
    ) -> datetime | None:
        pass

    @abstractmethod
    async def findTimerScriptSource(
        self,
        htmlString: str | Any | None
    ) -> str | None:
        pass
