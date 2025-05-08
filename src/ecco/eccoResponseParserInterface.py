from abc import ABC, abstractmethod
from typing import Any

from .models.eccoTimerData import EccoTimerData


class EccoResponseParserInterface(ABC):

    @abstractmethod
    async def parseTimerData(
        self,
        htmlString: str | Any | None
    ) -> EccoTimerData | None:
        pass
