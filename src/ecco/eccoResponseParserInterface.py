from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from .models.eccoTimerData import EccoTimerData


class EccoResponseParserInterface(ABC):

    @abstractmethod
    async def findTimerDateValue(
        self,
        htmlString: str | Any | None
    ) -> datetime | None:
        pass

    @abstractmethod
    async def findTimerScriptSource(
        self,
        htmlString: str | Any | None
    ) -> str | None:
        pass

    @abstractmethod
    async def parseTimerData(
        self,
        htmlString: str | Any | None
    ) -> EccoTimerData | None:
        pass
