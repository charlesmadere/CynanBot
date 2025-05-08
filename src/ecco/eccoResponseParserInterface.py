from abc import ABC, abstractmethod
from typing import Any

from .models.eccoResponse import EccoResponse


class EccoResponseParserInterface(ABC):

    @abstractmethod
    async def parseResponse(
        self,
        htmlContents: Any | None
    ) -> EccoResponse | None:
        pass
