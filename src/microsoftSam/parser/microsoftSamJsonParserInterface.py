from abc import ABC, abstractmethod
from typing import Any

from ..models.microsoftSamVoice import MicrosoftSamVoice


class MicrosoftSamJsonParserInterface(ABC):

    @abstractmethod
    async def parseVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice | None:
        pass

    @abstractmethod
    async def requireVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice:
        pass

    @abstractmethod
    async def serializeVoice(self, voice: MicrosoftSamVoice) -> str:
        pass
