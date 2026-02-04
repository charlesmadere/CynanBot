from abc import ABC, abstractmethod
from typing import Any

from ..models.microsoftTtsVoice import MicrosoftTtsVoice


class MicrosoftTtsJsonParserInterface(ABC):

    @abstractmethod
    async def parseVoice(
        self,
        string: str | Any | None,
    ) -> MicrosoftTtsVoice | None:
        pass

    @abstractmethod
    async def requireVoice(
        self,
        string: str | Any | None,
    ) -> MicrosoftTtsVoice:
        pass

    @abstractmethod
    async def serializeVoice(
        self,
        voice: MicrosoftTtsVoice,
    ) -> str:
        pass
