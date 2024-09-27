from abc import ABC, abstractmethod
from typing import Any

from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsJsonParserInterface(ABC):

    @abstractmethod
    async def parseVoice(self, jsonString: str | Any | None) -> StreamElementsVoice | None:
        pass

    @abstractmethod
    async def requireVoice(self, jsonString: str | Any | None) -> StreamElementsVoice:
        pass

    @abstractmethod
    async def serializeVoice(self, voice: StreamElementsVoice) -> str:
        pass
