from abc import ABC, abstractmethod
from typing import Any

from ..models.absPreferredTts import AbsPreferredTts


class ChatterPreferredTtsUserMessageHelperInterface(ABC):

    @abstractmethod
    async def parseUserMessage(
        self,
        userMessage: str | Any | None
    ) -> AbsPreferredTts | None:
        pass
