from abc import ABC, abstractmethod
from typing import Any

from ..models.absTtsProperties import AbsTtsProperties


class ChatterPreferredTtsUserMessageHelperInterface(ABC):

    @abstractmethod
    async def parseUserMessage(
        self,
        userMessage: str | Any | None,
    ) -> AbsTtsProperties | None:
        pass
