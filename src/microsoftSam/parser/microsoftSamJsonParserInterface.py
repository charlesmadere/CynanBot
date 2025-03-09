from abc import ABC, abstractmethod
from typing import Any

from ..models.microsoftSamVoice import MicrosoftSamVoice


class MicrosoftSamJsonParserInterface(ABC):

    @abstractmethod
    async def parseVoice(
        self,
        string: str | Any | None
    ) -> MicrosoftSamVoice | None:
        pass

    @abstractmethod
    async def requireVoice(
        self,
        string: str | Any | None
    ) -> MicrosoftSamVoice:
        pass

    @abstractmethod
    async def serializeVoice(
        self,
        voice: MicrosoftSamVoice
    ) -> str:
        pass
